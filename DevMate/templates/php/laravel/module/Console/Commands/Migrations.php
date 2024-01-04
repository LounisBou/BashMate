<?php 
namespace Modules\User\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Artisan;

class Migrations extends Command
{
    protected $signature = '[MODULE_NAME_TO_LOWER]:migrate'; // Command signature

    protected $description = 'Run [MODULE_NAME_TO_LOWER] module migrations';

    public function handle()
    {
        $this->info('Running [MODULE_NAME_TO_LOWER] module migrations...');

        // Call the migration command for the module
        Artisan::call('migrate', [
            '--path' => 'Modules/[MODULE_NAME]/Database/Migrations',
        ]);

        $this->info('[MODULE_NAME] module migrations completed.');
    }
}

// Path: app/Modules/[MODULE_NAME]/Console/Commands/Migrations.php
