local ts_utils = require 'nvim-treesitter.ts_utils'

local M = {}

function M.get_current_function_name()
  local current_node = ts_utils.get_node_at_cursor()
    if not current_node then
      return ""
    end

  local expr = current_node

  while expr do
      if expr:type() == 'function_definition' then
          break
      end
      expr = expr:parent()
  end

  if not expr then return "" end

  return (ts_utils.get_node_text(expr))
end

function M.send_current_function(channel_id)
  vim.rpcnotify(channel_id, 'code_change', 0, 'now', table.concat(M.get_current_function_name(), "\n"))
end

return M
