-- Cursor color
vim.api.nvim_set_hl(0, 'Cursor', { bg = '#000000', fg = '#ffffff' })
vim.api.nvim_set_hl(0, 'CursorIM', { bg = '#000000', fg = '#ffffff' })
vim.opt.guicursor = 'n-v-c:block-Cursor,i-ci-ve:ver25-Cursor,r-cr:hor20-Cursor'

-- Cmd+C (kitty keyboard protocol sequence) → system clipboard yank
vim.cmd([[set <F13>=\e[67;9u]])
vim.keymap.set('v', '<F13>', '"+y')
vim.keymap.set('n', '<F13>', '<Nop>')
vim.keymap.set('i', '<F13>', '<Esc>')
