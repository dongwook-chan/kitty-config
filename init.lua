-- Cmd+C → system clipboard yank
-- kitty sends \x1b[67;9u (67='C' uppercase), neovim maps this to <D-C>
local function map_cmd_c(mode, action)
  vim.keymap.set(mode, '<D-c>', action)
  vim.keymap.set(mode, '<D-C>', action)
end

map_cmd_c('x', '"+ygv')   -- visual mode: copy + keep selection
map_cmd_c('s', '<Nop>')   -- select mode: do nothing (kitty already copied)
map_cmd_c('n', '<Nop>')   -- normal mode: do nothing
map_cmd_c('i', '<Nop>')   -- insert mode: do nothing
