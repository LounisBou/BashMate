<?php 
namespace Modules\User\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Artisan;

class Seeders extends Command
{
    protected $signature = '[MODULE_NAME_TO_LOWER]:seed'; // Command signature

    protected $description = 'Run [MODULE_NAME_TO_LOWER] module seeders';

    public function handle()
    {
        $this->info('Running [MODULE_NAME_TO_LOWER] module seeders...');

        // Call the migration command for the module
        Artisan::call('db:seed', [
            '--class' => \Modules\[MODULE_NAME]\Database\Seeders\Seeder::class, // Path to seeder class
        ]);

        $this->info('[MODULE_NAME] module seeders completed.');
    }
}

// Path: app/Modules/[MODULE_NAME]/Console/Commands/Seeders.php
