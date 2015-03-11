-- **************************************************************************************************************
-- **************************************************************************************************************
--
--	Name: 		core.lua
--	Author:		Paul Robson (paul@robsons.org.uk)
--	Purpose:	Core files
--	Created: 	11th March 2015
--	Released:	-
--	Version:	0.1
--
-- **************************************************************************************************************
-- **************************************************************************************************************

_G["__CWRBaseObject"] = {}															-- this is the object

local baseObject = _G.__CWRBaseObject 												-- and a short term reference to it

baseObject.classes = {} 															-- class name => definition.

local parentClass = {} 																-- final super class for all objects
parentClass.__index = parentClass

local index = { _object = {} } 														-- tag name => index data
local indexCount = { _object = 0 } 													-- tag name => index count

baseObject.__index = index 															-- make index accessible for
baseObject.__indexCount = indexCount 												-- helper functions.

-- **************************************************************************************************************
--- @method 	[BASE].__registerClass
--- Register a new class with the given name and optional superclass
---	@param 	name 		string 		Class name (case insensitive)
--- @param  superclass 	string 		Name of superclass.
--- @return 			table/table The prototype and the superclass references.
-- **************************************************************************************************************

function baseObject.__registerClass(name,superClass)
	assert(name ~= nil and type(name) == "string")									-- parameter check
	if superClass ~= nil then 														-- superclass provided.
		assert(type(superClass) == "string")										-- type check/exist check
		assert(baseObject.classes[superClass] ~= nil,"Class "..superClass.. "not defined")
		superClass = baseObject.classes[superClass]									-- then use that as the superclass.
	else
		superClass = parentClass													-- otherwise use the parent class.
	end
	name = name:lower()																-- name is case insensitive.
	assert(baseObject.classes[name] == nil,"Class "..name.." defined twice")		-- check multiple definitions
	local newClass = {}																-- create a new class.
	newClass.__index = newClass 													-- set it up appropriately.
	setmetatable(newClass,superClass)												-- set the super class
	baseObject.classes[name] = newClass 											-- save definition.
	return newClass,superClass 	
end

-- **************************************************************************************************************
---	@method 	[BASE].__new
---	Create a new instance of the requested class. Tags it as _object, and sets the alive flag.
---	@param 	name 		string 		Class name (case insensitive)
---	@param 	consData 	table 		Constructor data.
---	@return 			table 		New instance of requested class.
-- **************************************************************************************************************

function baseObject.__new(name,consData)
	consData = consData or {}														-- default constructor data
	assert(name ~= nil and type(name) == "string")									-- parameter check
	assert(type(consData) == "table")
	name = name:lower()																-- name is case insensitive.
	assert(baseObject.classes[name] ~= nil,"Class "..name.." not defined")			-- check class exists.

	local newInstance = {}															-- this is the new instance.
	setmetatable(newInstance,baseObject.classes[name])								-- set the metatable.
	if newInstance.__constructor ~= nil then 										-- is there a constructor ?
		newInstance:__constructor(consData)											-- then call it
	end
	index._object[newInstance] = newInstance 										-- add to object index
	indexCount._object = indexCount._object + 1 									-- increment the object counter.
	newInstance.__isAliveFlag = true 												-- object is now alive.
	return newInstance																-- return the new instance.
end

-- **************************************************************************************************************
--- @method 	[ROOT].__destroy()
---	Destroys the referred object - clearing the alive flag, removing from the index, calling the destructor
---	defined.
-- **************************************************************************************************************

function parentClass:destroy() 
	assert(self.__isAliveFlag,"Object has been destroyed already.")					-- can't destroy twice.
	self.__isAliveFlag = false 														-- mark as not alive.
	index._object[self] = nil 														-- remove from index
	indexCount._object = indexCount._object - 1 									-- adjust the index count.
	if self.__destructor ~= nil then 												-- if destructor exists
		self:__destructor()															-- call it
	end
end

-- **************************************************************************************************************
--- @method 	[ROOT].__isAlive()
---	Checks to see if the referenced object is still alive.
---	@return 	boolean 	true if it is still alive.
-- **************************************************************************************************************

function parentClass:__isAlive()
	return self.__isAliveFlag														-- just returns the alive flag.
end 

require("_test")

--[[
class = baseObject.__registerClass("demo.class")
class.x = 1
class.__constructor = function(self,a) print("Constructor",a.q,a.w) end 
function class:__destructor() print("Destructor") end

class2 = baseObject.__registerClass("demo.class2","demo.class")
class2.x2 = 3

parentClass.test = 42

z = baseObject.__new("demo.class2",{ q = 12,w = 44 })
print(z.x,z.test,parentClass.test)
print(z:__isAlive())
z:destroy()
print(z:__isAlive())
--]]

-- **************************************************************************************************************
--	Date		Version		Notes
--	====		=======		=====
--	11-Mar-15	0.1 		First created
--
-- **************************************************************************************************************