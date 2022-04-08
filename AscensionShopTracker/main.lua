-- Ascension Shop Tracker
-- Author: sweepline
local N, NS = ...

local function add_price_information(tooltip)
    local _, item_link = tooltip:GetItem()
    if item_link ~= nil then
        local item_id = select(3, item_link:find("item:(%d+)"))
        item_id = tonumber(item_id)
        if item_id ~= nil then
	    local data_item = NS.data[item_id]
	    if data_item ~= nil then
                local price = data_item.item_price
		local d_price = data_item.discount_price
		-- Color codes are `|cAARRGGBBTEXT|r`
		if d_price ~= nil then
                    tooltip:AddLine("|cFFFFFFFFShop price:|r |cFFFF6060" .. d_price .. " |cFFFFFFFFDP|r")
		    local discount = ((price - d_price) / price) * 100
                    tooltip:AddLine("|cFFFFFFFF- This is a|r |cFFFF6060" .. discount .. "%|r |cFFFFFFFFdiscount|r")
		else
                    tooltip:AddLine("|cFFFFFFFFShop price:|r " .. price .. " |cFFFFFFFFDP|r")
		end
	    end
        end
    end
end

--- Hook to Tooltip
GameTooltip:HookScript("OnTooltipSetItem", add_price_information)
