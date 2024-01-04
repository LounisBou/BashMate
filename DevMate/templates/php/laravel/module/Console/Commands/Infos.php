<?php 
namespace Modules\User\Console\Commands;

use Illuminate\Console\Command;

class Infos extends Command
{
    protected $signature = '[MODULE_NAME_TO_LOWER]:info'; // Command signature

    protected $description = 'Display information about the [MODULE_NAME] module';

    public function handle()
    {
        // Logic to retrieve module information
        $this->line('[MODULE_NAME] module information:');
        $this->table(['Module Name', 'Description'], [
            ['[MODULE_NAME]', '[MODULE_DESCRIPTION]'],
        ]);
    }
}

// Path: app/Modules/[MODULE_NAME]/Console/Commands/Infos.php