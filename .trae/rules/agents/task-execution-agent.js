#!/usr/bin/env node

/**
 * Task Execution Agent
 * Automatically executes tasks from tasks.md files using checkbox state
 */

const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');

class TaskExecutionAgent {
    constructor() {
        this.tasksFilePath = null;
        this.tasks = [];
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
                    return files[0]; // Return first tasks.md found
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
            // Match both unchecked and checked tasks
            const taskMatch = line.match(/- \[( |x)\] \*\*Task ([\d.]+):\*\*(.+)$/);
            if (taskMatch) {
                const completed = taskMatch[1] === 'x';
                const taskId = taskMatch[2];
                const taskTitle = taskMatch[3].trim();
                const description = [];
                
                // Read description lines (indented lines following the task)
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
        const task = this.tasks.find(t => t.id === taskId);
        if (!task) {
            throw new Error(`Task ${taskId} not found`);
        }

        // Read current file content
        const content = await fs.readFile(this.tasksFilePath, 'utf-8');
        const lines = content.split('\n');
        
        // Find and update the task line
        const taskLinePattern = new RegExp(`- \\[ \\] \\*\\*Task ${taskId.replace(/\./g, '\\.')}:\\*\\*`);
        for (let i = 0; i < lines.length; i++) {
            if (taskLinePattern.test(lines[i])) {
                lines[i] = lines[i].replace('- [ ]', '- [x]');
                break;
            }
        }
        
        // Write back to file
        await fs.writeFile(this.tasksFilePath, lines.join('\n'));
        task.completed = true;
        console.log(`✅ Marked Task ${taskId} as completed in ${this.tasksFilePath}`);
    }

    async executeTask(task) {
        console.log(`\n=== Executing Task ${task.id}: ${task.title} ===`);
        console.log(`Description: ${task.description}`);

        try {
            // Execute the /spec-execute-task command
            const command = `claude-code /spec-execute-task ${task.id}`;
            console.log(`Running: ${command}`);
            
            execSync(command, { 
                stdio: 'inherit',
                cwd: process.cwd(),
                timeout: 30 * 60 * 1000 // 30 minutes timeout
            });
            
            // Mark task as completed in tasks.md
            await this.markTaskCompleted(task.id);
            console.log(`✅ Task ${task.id} completed successfully`);
            
        } catch (error) {
            console.error(`❌ Task ${task.id} failed:`, error.message);
            throw error;
        }
    }

    async executeAllTasks() {
        try {
            const tasksFile = await this.findTasksFile();
            console.log(`Found tasks file: ${tasksFile}`);
            
            const tasks = await this.parseTasksFile(tasksFile);
            console.log(`Found ${tasks.length} tasks in file`);
            
            // Filter out completed tasks
            const pendingTasks = tasks.filter(task => !task.completed);
            const completedTasks = tasks.filter(task => task.completed);
            
            console.log(`Completed tasks: ${completedTasks.length}`);
            console.log(`Pending tasks: ${pendingTasks.length}`);
            
            if (pendingTasks.length === 0) {
                console.log('🎉 All tasks completed!');
                return;
            }
            
            let successCount = completedTasks.length;
            let failCount = 0;
            
            for (const task of pendingTasks) {
                try {
                    await this.executeTask(task);
                    successCount++;
                } catch (error) {
                    console.error(`Task ${task.id} failed, continuing with next task...`);
                    failCount++;
                    // Continue with next task even if current one fails
                }
            }
            
            console.log(`\n=== Execution Summary ===`);
            console.log(`Total tasks: ${tasks.length}`);
            console.log(`Completed: ${successCount}`);
            console.log(`Failed: ${failCount}`);
            console.log(`Success rate: ${((successCount / tasks.length) * 100).toFixed(1)}%`);
            
            if (successCount === tasks.length) {
                console.log('🎉 All tasks completed successfully!');
            } else if (failCount > 0) {
                console.log('⚠️  Some tasks failed. You can retry by running this script again.');
            }
            
        } catch (error) {
            console.error('Fatal error:', error.message);
            process.exit(1);
        }
    }

    async resetAllTasks() {
        try {
            const tasksFile = await this.findTasksFile();
            const content = await fs.readFile(tasksFile, 'utf-8');
            
            // Replace all checked tasks with unchecked
            const updatedContent = content.replace(/- \[x\] \*\*Task/g, '- [ ] **Task');
            
            await fs.writeFile(tasksFile, updatedContent);
            console.log('✅ All tasks reset to unchecked state');
            
        } catch (error) {
            console.error('Error resetting tasks:', error.message);
        }
    }

    async showStatus() {
        try {
            const tasksFile = await this.findTasksFile();
            console.log(`Tasks file: ${tasksFile}`);
            
            const tasks = await this.parseTasksFile(tasksFile);
            const completedTasks = tasks.filter(task => task.completed);
            const pendingTasks = tasks.filter(task => !task.completed);
            
            console.log(`\n=== Task Status ===`);
            console.log(`Total tasks: ${tasks.length}`);
            console.log(`Completed: ${completedTasks.length}`);
            console.log(`Pending: ${pendingTasks.length}`);
            console.log(`Progress: ${((completedTasks.length / tasks.length) * 100).toFixed(1)}%`);
            
            if (pendingTasks.length > 0) {
                console.log(`\nNext pending tasks:`);
                pendingTasks.slice(0, 5).forEach(task => {
                    console.log(`  - Task ${task.id}: ${task.title}`);
                });
                if (pendingTasks.length > 5) {
                    console.log(`  ... and ${pendingTasks.length - 5} more`);
                }
            }
            
        } catch (error) {
            console.error('Error showing status:', error.message);
        }
    }
}

// CLI Interface
async function main() {
    const agent = new TaskExecutionAgent();
    const args = process.argv.slice(2);
    
    switch (args[0]) {
        case 'reset':
            await agent.resetAllTasks();
            break;
        case 'status':
            await agent.showStatus();
            break;
        case 'execute-next':
            // Execute only the next pending task
            try {
                const tasksFile = await agent.findTasksFile();
                const tasks = await agent.parseTasksFile(tasksFile);
                const nextTask = tasks.find(task => !task.completed);
                if (nextTask) {
                    await agent.executeTask(nextTask);
                } else {
                    console.log('🎉 All tasks completed!');
                }
            } catch (error) {
                console.error('Error executing next task:', error.message);
            }
            break;
        case 'retry-failed':
            console.log('Note: Failed tasks are no longer tracked separately. Use status to see pending tasks.');
            await agent.showStatus();
            break;
        default:
            await agent.executeAllTasks();
    }
}

if (require.main === module) {
    main().catch(console.error);
}

module.exports = TaskExecutionAgent;