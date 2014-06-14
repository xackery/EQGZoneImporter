
local list = iup.list{visiblecolumns = 12, visiblelines = 15, expand = "VERTICAL"}
local data, region, fields, active_pos
local tonumber = tonumber

function list:action(str, pos, state)
	if state == 1 and data then
		active_pos = pos
		region = data[pos]
		for k, field in pairs(fields) do
			field.value = region[k]
		end
	end
end

local function Edited()
	if region then
		for k, field in pairs(fields) do
			region[k] = (k == "name") and field.value or tonumber(field.value)
		end
		if active_pos then
			list[active_pos] = fields.name.value or ""
		end
	end
end

fields = {
	name = iup.text{visiblecolumns = 16, valuechanged_cb = Edited},
	center_x = iup.text{visiblecolumns = 16, mask = iup.MASK_FLOAT, valuechanged_cb = Edited},
	center_y = iup.text{visiblecolumns = 16, mask = iup.MASK_FLOAT, valuechanged_cb = Edited},
	center_z = iup.text{visiblecolumns = 16, mask = iup.MASK_FLOAT, valuechanged_cb = Edited},
	unknownA = iup.text{visiblecolumns = 16, mask = iup.MASK_FLOAT, valuechanged_cb = Edited},
	unknownB = iup.text{visiblecolumns = 16, mask = iup.MASK_UINT, valuechanged_cb = Edited},
	unknownC = iup.text{visiblecolumns = 16, mask = iup.MASK_UINT, valuechanged_cb = Edited},
	extent_x = iup.text{visiblecolumns = 16, mask = iup.MASK_FLOAT, valuechanged_cb = Edited},
	extent_y = iup.text{visiblecolumns = 16, mask = iup.MASK_FLOAT, valuechanged_cb = Edited},
	extent_z = iup.text{visiblecolumns = 16, mask = iup.MASK_FLOAT, valuechanged_cb = Edited},
}

local grid = iup.gridbox{
	iup.label{title = "Name"}, fields.name,
	iup.label{title = "Center X"}, fields.center_x,
	iup.label{title = "Center Y"}, fields.center_y,
	iup.label{title = "Center Z"}, fields.center_z,
	iup.label{title = "Unknown A"}, fields.unknownA,
	iup.label{title = "Unknown B"}, fields.unknownB,
	iup.label{title = "Unknown C"}, fields.unknownC,
	iup.label{title = "Extent X"}, fields.extent_x,
	iup.label{title = "Extent Y"}, fields.extent_y,
	iup.label{title = "Extent Z"}, fields.extent_z,
	numdiv = 2, orientation = "HORIZONTAL", homogeneouslin = "YES",
	gapcol = 10, gaplin = 8, alignmentlin = "ACENTER", sizelin = 6
}

local function ClearFields()
	for _, field in pairs(fields) do
		field.value = ""
	end
end

local function read(ter_data, zon_data)
	active_pos = nil
	data = zon_data.regions
	list.autoredraw = "NO"
	list[1] = nil
	for i, reg in ipairs(zon_data.regions) do
		list[i] = reg.name
	end
	list.autoredraw = "YES"
	ClearFields()
end

local function AddRegion()
	if data then
		table.insert(data, {
			name = "Unnamed",
			center_x = 0, center_y = 0, center_z = 0,
			extent_x = 0, extent_y = 0, extent_z = 0,
			unknownA = 0, unknownB = 0, unknownC = 0,
		})
		list[tonumber(list.count) + 1] = "Unnamed"
	end
end

local function CopyRegion()
	if data and region then
		local new = {}
		for k, v in pairs(region) do
			new[k] = v
		end
		table.insert(data, new)
		list[tonumber(list.count) + 1] = new.name or "Unnamed"
	end
end

local function DeleteRegion()
	if data and active_pos then
		table.remove(data, active_pos)
		list.autoredraw = "NO"
		list[1] = nil
		for i, reg in ipairs(data) do
			list[i] = reg.name
		end
		list.autoredraw = "YES"
		ClearFields()
		active_pos = nil
		region = nil
	end
end

function list:button_cb(button, pressed, x, y)
	if data and button == iup.BUTTON3 and pressed == 0 then
		local mx, my = iup.GetGlobal("CURSORPOS"):match("(%d+)x(%d+)")
		local menu = iup.menu{
			iup.item{title = "Add Region", action = AddRegion},
			iup.item{title = "Copy Region", action = CopyRegion, active = region and "YES" or "NO"},
			iup.separator{},
			iup.item{title = "Remove Region", action = DeleteRegion, active = active_pos and "YES" or "NO"},
		}
		iup.Popup(menu, mx, my)
		iup.Destroy(menu)
	end
end

return {
	name = "Regions",
	display = iup.hbox{list, grid; nmargin = "10x10", gap = 10},
	read = read,
}
