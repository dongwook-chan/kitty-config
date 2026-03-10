-- Cmd+C (kitty keyboard protocol sequence) → system clipboard yank
vim.cmd([[set <F13>=\e[67;9u]])
vim.keymap.set('v', '<F13>', '"+ygv')
vim.keymap.set('n', '<F13>', '<Nop>')
vim.keymap.set('i', '<F13>', '<Esc>')
