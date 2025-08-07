#!/usr/bin/env node

/**
 * Auto Task Executor
 * Automatically takes over after /spec-execute-task and continues executing all remaining tasks
 */

const fs = require('fs').promises;
const path = require('path');
const { spawn } = require('child_process');

class AutoTaskExecutor {
    constructor() {
        this.tasksFilePath = null;
        this.tasks = [];
        this.isExecuting = false;
        this.lockFile = '.claude/execution-lock';
        this.statusFile = '.claude/execution-status.json';
    }

    async createExecutionLock() {
        await fs.mkdir(path.dirname(this.lockFile), { recursive: true });
        await fs.writeFile(this.lockFile, JSON.stringify({
            started: new Date().toISOString(),
            pid: process.pid
        }));
    }

    async removeExecutionLock() {
        try {
            await fs.unlink(this.lockFile);
        } catch (error) {
            // Ignore if file doesn't exist
        }
    }

    async saveExecutionStatus(status) {
        const statusData = {
            ...status,
            timestamp: new Date().toISOString()
        };
        await fs.mkdir(path.dirname(this.statusFile), { recursive: true });
        await fs.writeFile(this.statusFile, JSON.stringify(statusData, null, 2));
    }

    async findTasksFile() {
        const searchPaths = [
            '.claude/specs/*/tasks.md',
            '.qwen/specs/*/tasks.md'
        ];

        for (const pattern of searchPaths) {
            try {
                const files = await this.glob(pattern);
                if (files.length > 0) {
                    return files[0];
                }
            } catch (error) {
                continue;
            }
        }
        throw new Error('No tasks.md file found');
    }

    async glob(pattern) {
        const { glob } = require('glob');
        return glob(pattern, { cwd: process.cwd() });
    }

    async parseTasksFile(filePath) {
        const content = await fs.readFile(filePath, 'utf-8');
        this.tasksFilePath = filePath;
        const tasks = [];
        const lines = content.split('\n');
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const taskMatch = line.match(/- \[( |x)\] \*\*Task ([\d.]+):\*\*(.+)$/);
            if (taskMatch) {
                const completed = taskMatch[1] === 'x';
                const taskId = taskMatch[2];
                const taskTitle = taskMatch[3].trim();
                const description = [];
                
                let j = i + 1;
                while (j < lines.length && lines[j].startsWith('  ')) {
                    description.push(lines[j].trim());
                    j++;
                }
                
                tasks.push({
                    id: taskId,
                    title: taskTitle,
                    description: description.join(' '),
                    completed: completed,
                    lineNumber: i
                });
            }
        }
        
        this.tasks = tasks;
        return tasks;
    }

    async markTaskCompleted(taskId) {
        const content = await fs.readFile(this.tasksFilePath, 'utf-8');
        const lines = content.split('\n');
        
        const taskLinePattern = new RegExp(`- \\[ \\] \\*\\*Task ${taskId.replace(/\./g, '\\.')}:\\*\\*`);
        for (let i = 0; i < lines.length; i++) {
            if (taskLinePattern.test(lines[i])) {
                lines[i] = lines[i].replace('- [ ]', '- [x]');
                break;
            }
        }
        
        await fs.writeFile(this.tasksFilePath, lines.join('\n'));
        console.log(`✅ Task ${taskId} marked as completed`);
    }

    async executeTask(task) {
        console.log(`\n🚀 Auto-executing Task ${task.id}: ${task.title}`);
        console.log(`Description: ${task.description}`);

        await this.saveExecutionStatus({
            currentTask: task.id,
            status: 'executing',
            progress: `${this.tasks.filter(t => t.completed).length}/${this.tasks.length}`
        });

        return new Promise((resolve, reject) => {
            // Execute the /spec-execute-task using Task tool with spec-task-reviewer agent
            const command = 'claude';
            const args = ['task', 'spec-task-reviewer', `/spec-execute-task ${task.id}`];
            
            console.log(`Executing: ${command} ${args.join(' ')}`);
            
            const child = spawn(command, args, {
                stdio: 'inherit',
                cwd: process.cwd(),
                shell: true
            });

            let timeout = setTimeout(() => {
                child.kill('SIGTERM');
                reject(new Error(`Task ${task.id} timed out after 30 minutes`));
            }, 30 * 60 * 1000);

            child.on('close', async (code) => {
                clearTimeout(timeout);
                
                if (code === 0) {
                    try {
                        await this.markTaskCompleted(task.id);
                        task.completed = true;
                        console.log(`✅ Task ${task.id} completed successfully`);
                        resolve();
                    } catch (error) {
                        console.error(`Error marking task completed: ${error.message}`);
                        reject(error);
                    }
                } else {
                    const error = new Error(`Task ${task.id} failed with exit code ${code}`);
                    console.error(`❌ ${error.message}`);
                    reject(error);
                }
            });

            child.on('error', (error) => {
                clearTimeout(timeout);
                console.error(`❌ Task ${task.id} execution error:`, error.message);
                reject(error);
            });
        });
    }

    async executeAllRemainingTasks() {
        try {
            await this.createExecutionLock();
            this.isExecuting = true;

            const tasksFile = await this.findTasksFile();
            console.log(`📋 Found tasks file: ${tasksFile}`);
            
            const tasks = await this.parseTasksFile(tasksFile);
            const pendingTasks = tasks.filter(task => !task.completed);
            const completedTasks = tasks.filter(task => task.completed);
            
            console.log(`📊 Total tasks: ${tasks.length}`);
            console.log(`✅ Completed: ${completedTasks.length}`);
            console.log(`⏳ Pending: ${pendingTasks.length}`);
            
            if (pendingTasks.length === 0) {
                console.log('🎉 All tasks already completed!');
                await this.saveExecutionStatus({
                    status: 'completed',
                    message: 'All tasks completed successfully'
                });
                return;
            }

            console.log(`\n🤖 Auto-executor taking over! Will execute ${pendingTasks.length} remaining tasks...`);
            
            let successCount = completedTasks.length;
            let failCount = 0;
            
            for (let i = 0; i < pendingTasks.length; i++) {
                const task = pendingTasks[i];
                
                console.log(`\n[${i + 1}/${pendingTasks.length}] Starting Task ${task.id}...`);
                
                try {
                    await this.executeTask(task);
                    successCount++;
                    console.log(`Progress: ${successCount}/${tasks.length} tasks completed`);
                    
                    // Small delay between tasks
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    
                } catch (error) {
                    failCount++;
                    console.error(`Task ${task.id} failed: ${error.message}`);
                    console.log(`Continuing with next task...`);
                    
                    await this.saveExecutionStatus({
                        currentTask: task.id,
                        status: 'failed',
                        error: error.message,
                        progress: `${successCount}/${tasks.length}`
                    });
                }
            }
            
            // Final summary
            console.log(`\n🏁 === Execution Complete ===`);
            console.log(`📊 Total tasks: ${tasks.length}`);
            console.log(`✅ Completed: ${successCount}`);
            console.log(`❌ Failed: ${failCount}`);
            console.log(`📈 Success rate: ${((successCount / tasks.length) * 100).toFixed(1)}%`);
            
            const finalStatus = successCount === tasks.length ? 'all-completed' : 'completed-with-failures';
            await this.saveExecutionStatus({
                status: finalStatus,
                totalTasks: tasks.length,
                completed: successCount,
                failed: failCount,
                successRate: ((successCount / tasks.length) * 100).toFixed(1)
            });
            
            if (successCount === tasks.length) {
                console.log('🎉 All tasks completed successfully! Auto-execution finished.');
            } else {
                console.log('⚠️  Some tasks failed. You can review and retry manually if needed.');
            }
            
        } catch (error) {
            console.error('💥 Fatal error in auto-execution:', error.message);
            await this.saveExecutionStatus({
                status: 'fatal-error',
                error: error.message
            });
        } finally {
            this.isExecuting = false;
            await this.removeExecutionLock();
        }
    }

    async stopExecution() {
        if (this.isExecuting) {
            console.log('🛑 Stopping auto-execution...');
            this.isExecuting = false;
            await this.removeExecutionLock();
            await this.saveExecutionStatus({
                status: 'stopped',
                message: 'Execution stopped by user'
            });
        } else {
            console.log('ℹ️  No active execution to stop');
        }
    }

    async showStatus() {
        try {
            const tasksFile = await this.findTasksFile();
            const tasks = await this.parseTasksFile(tasksFile);
            const completedTasks = tasks.filter(task => task.completed);
            const pendingTasks = tasks.filter(task => !task.completed);
            
            console.log(`📋 Tasks file: ${tasksFile}`);
            console.log(`📊 Total tasks: ${tasks.length}`);
            console.log(`✅ Completed: ${completedTasks.length}`);
            console.log(`⏳ Pending: ${pendingTasks.length}`);
            console.log(`📈 Progress: ${((completedTasks.length / tasks.length) * 100).toFixed(1)}%`);
            
            try {
                const statusContent = await fs.readFile(this.statusFile, 'utf-8');
                const status = JSON.parse(statusContent);
                console.log(`\n🤖 Last execution status: ${status.status}`);
                if (status.currentTask) {
                    console.log(`Current/Last task: ${status.currentTask}`);
                }
                console.log(`Updated: ${status.timestamp}`);
            } catch (error) {
                console.log('\nℹ️  No execution status available');
            }
            
        } catch (error) {
            console.error('Error showing status:', error.message);
        }
    }
}

// CLI Interface
async function main() {
    const executor = new AutoTaskExecutor();
    const args = process.argv.slice(2);
    
    switch (args[0]) {
        case 'auto-start':
        case 'force-start':
        case 'resume-execution':
            console.log('🤖 Starting automatic task execution...');
            await executor.executeAllRemainingTasks();
            break;
            
        case 'continue-execution':
            // This is triggered when a task is marked complete
            // Check if there are more tasks and continue
            console.log('🔄 Continuing automatic execution...');
            await executor.executeAllRemainingTasks();
            break;
            
        case 'stop':
            await executor.stopExecution();
            break;
            
        case 'status':
            await executor.showStatus();
            break;
            
        default:
            console.log('🤖 Auto Task Executor');
            console.log('Available commands:');
            console.log('  auto-start    - Start automatic execution');
            console.log('  stop          - Stop execution');
            console.log('  status        - Show current status');
    }
}

if (require.main === module) {
    main().catch(console.error);
}

module.exports = AutoTaskExecutor;