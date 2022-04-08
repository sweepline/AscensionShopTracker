local data = require("data")

local item_link = "|cff0070dd|Hitem:99077::::::::53:257::2:1:4198:2:28:1199:9:35:::::|h[Missing Diplomat's Pauldrons]|h|r"

print(data[99077].item_price)
local function add_price_information()
    if item_link ~= nil then
		local item_id = select(3, item_link:find("item:(%d+)"))
		item_id = tonumber(item_id)
		if item_id ~= nil then
			print(data[item_id])
			local price = data[item_id].item_price
			print(price)
			return "Shop price " .. price .. " DP"
		end
    end
end

print(add_price_information())
