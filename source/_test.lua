
baseObject = __CWRBaseObject														-- access the global
classCount = 20																		-- number of objects
objectCount = 100																	-- number of tags.
runs = 10 																			-- number of runs.
math.randomseed(42)
classNames = {}																		-- create classes
for i = 1,classCount do 
	classNames[i] = "test.class"..i 
	baseObject.__registerClass(classNames[i])
end

objectRefs = {}																		-- null object ref array.
for i = 1,objectCount do objectRefs[i] = nil end 

for r = 1,runs do 																	-- run the tests.
	if r % 1000 == 0 then print("Pass "..r) end 									-- show progress.

	-- Pick an object randomly - create it if it is free, delete it if it isn't.

	obj = math.random(1,objectCount)												-- pick an object
	if objectRefs[obj] == nil then 													-- if it doesn't exist.
		objectRefs[obj] = baseObject.__new(classNames[math.random(1,classCount)])	-- create one randomly.
	else 
		objectRefs[obj]:destroy()													-- otherwise destroy and null it.
		objectRefs[obj] = nil
	end

	-- Check the _object index is maintained correctly.
																					-- check the _object index.
	c = 0																			-- count of object.
	for i = 1,objectCount do 														-- go through each object
		if objectRefs[i] ~= nil then 
			c = c + 1
			assert(baseObject.__index._object[objectRefs[i]] == objectRefs[i])
		end
	end
	assert(baseObject.__indexCount._object == c)									-- check the object counts match

	c = 0 																			-- count the number of objects in
	for i,_ in pairs(baseObject.__index._object) do c = c + 1 end					-- the physical index
	assert(baseObject.__indexCount._object == c)									-- check the object counts match

end

print("Completed.")