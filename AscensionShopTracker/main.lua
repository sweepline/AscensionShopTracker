-- Ascension Shop Tracker
-- Author: sweepline
local N, NS = ...

local function add_price_information(tooltip)
    local _, item_link = tooltip:GetItem()
    if item_link ~= nil then
        local item_id = select(3, item_link:find("item:(%d+)"))
        item_id = tonumber(item_id)
        if item_id ~= nil then
            local price = NS.data[item_id].item_price
            tooltip:AddLine("Shop price " .. price .. " DP")
        end
    end
end

--- Hook to Tooltip
GameTooltip:HookScript("OnTooltipSetItem", add_price_information)
