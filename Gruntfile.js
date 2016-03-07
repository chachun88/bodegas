/* global module */
/* global require */

'use strict';

module.exports = function(grunt)
{
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        watch: {
          scripts: {
            files: ['**/*.py'],
            tasks: ['shell'],
            options: {
              spawn: false,
            },
          },
        },
        shell: {
            options: {
                failOnError: true,
                stderr: true,
                stdout: true,
                stdin: true
            },
            target: {
                command: 'python -m worker'
            }
        }
    });


    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.registerTask('worker', ['watch'])
};
