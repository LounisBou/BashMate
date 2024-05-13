" Vim settings

" Start plugin declaration block
call plug#begin()
" The default plugin directory will be as follows:
"   - Vim (Linux/macOS): '~/.vim/plugged'
"   - Vim (Windows): '~/vimfiles/plugged'
"   - Neovim (Linux/macOS/Windows): stdpath('data') . '/plugged'
" You can specify a custom plugin directory by passing it as the argument
"   - e.g. `call plug#begin('~/.vim/plugged')`
"   - Avoid using standard Vim directory names like 'plugin'

" Make sure you use single quotes

" Intellisense code completion
Plug 'neoclide/coc.nvim'

" Shortcuts
Plug 'liuchengxu/vim-which-key'

" Easy Align
Plug 'junegunn/vim-easy-align'

" Fuzzy Finder (Post-update hook)
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }

" Lightline
Plug 'itchyny/lightline.vim'

" GitGutter
Plug 'airblade/vim-gitgutter'

" File system explorer (On-demand loading: loaded when the specified command is executed)
Plug 'preservim/nerdtree', { 'on': 'NERDTreeToggle' }

" Warp cursor
Plug 'tpope/vim-surround'

" Smooth scrolling
Plug 'terryma/vim-smooth-scroll'

" CSS color preview
Plug 'ap/vim-css-color'

" Git Blame
Plug 'f-person/git-blame.nvim'

" A collection of awesome Vim colorschemes
Plug 'rafi/awesome-vim-colorschemes'

" Initialize plugin system
call plug#end()

" You can revert the settings after the call like so:
"   filetype indent off   " Disable file-type-specific indentation
"   syntax off            " Disable syntax highlighting

" Theme
set background=dark
colorscheme oceanic_material

" Syntax highlighting
syntax on

" Enable filetype detection
filetype plugin indent on

" Backspace delete char
set backspace=indent,eol,start

" Enable line numbers
set number

" Position in code
set number
set ruler

" Function to set tab width to n spaces
function! SetTab(n)
    let &l:tabstop=a:n
    let &l:softtabstop=a:n
    let &l:shiftwidth=a:n
    set expandtab
endfunction
command! -nargs=1 SetTab call SetTab(<f-args>)

" Set tab width to 4 spaces
SetTab 4

" Function to trim extra whitespace in whole file
function! Trim()
    let l:save = winsaveview()
    keeppatterns %s/\s\+$//e
    call winrestview(l:save)
endfun
command! -nargs=0 Trim call Trim()

" Shortcuts remapping

" Save file with Command + S
noremap <D-s> :w<CR>

" Trim whitespace with Command + T
noremap <D-t> :Trim<CR>

" Write & Quit with Command + W
noremap <D-w> :wq<CR>


