
baseObject = __CWRBaseObject														-- access the global
classCount = 30																		-- number of classes
tagCount = 30 																		-- number of tags.
objectCount = 200																	-- number of objects

runs = 100 																			-- number of runs.
tagChanges = 15 																	-- tag changes per run.

math.randomseed(42)
classNames = {}																		-- create classes
for i = 1,classCount do 
	classNames[i] = "test.class"..i 
	baseObject.__registerClass(classNames[i])
end

tagNames = {}
for i = 1,tagCount do tagNames[i] = "tag"..i end 									-- create tag names.

objectRefs = {}																		-- object ref array.
objectHasTag = {}																	-- array of array of has tags or not.
for i = 1,objectCount do 
	objectRefs[i] = nil
	objectHasTag[i] = {}
	for j = 1,tagCount do objectHasTag[i][j] = false end
end 

for r = 1,runs do 																	-- run the tests.
	if r % 1000 == 0 then print("Pass "..r) end 									-- show progress.

	-- Pick an object randomly - create it if it is free, delete it if it isn't.

	obj = math.random(1,objectCount)												-- pick an object
	if objectRefs[obj] == nil then 													-- if it doesn't exist.
		objectRefs[obj] = baseObject.__new(classNames[math.random(1,classCount)])	-- create one randomly.
		assert(objectRefs[obj]:__isAlive() == true)
	else 
		if math.random(1,4) == 1 then 												-- one chance in four
			assert(objectRefs[obj]:__isAlive() == true)
			objectRefs[obj]:destroy()												-- destroy and null it.
			assert(objectRefs[obj]:__isAlive() == false)
			objectRefs[obj] = nil
			for i = 1,tagCount do objectHasTag[obj][i] = false end					-- and it has no tags.
		end
	end

	-- Change tags randomly on objects 

	for tc = 1,tagChanges do 	
		obj = math.random(1,objectCount)
		if objectRefs[obj] ~= nil then 
			tag = math.random(1,tagCount)
			if math.random(1,5) <= 3 then 
				objectRefs[obj]:__tag(tagNames[tag])
				objectHasTag[obj][tag] = true
			else
				objectRefs[obj]:__untag(tagNames[tag])
				objectHasTag[obj][tag] = false
			end
		end
	end

	-- Check the tag counts in the indices are correct, and that tags are correct.

	for tag = 1,tagCount do 
		c = 0
		for i = 1,objectCount do 
			if objectHasTag[i][tag] then 
				c = c + 1 
				assert(baseObject.__index[tagNames[tag]][objectRefs[i]] ~= nil)
			end
		end 
	end

	-- Check the _object index is maintained correctly.
																					-- check the _object index.
	c = 0																			-- count of object.
	for i = 1,objectCount do 														-- go through each object
		if objectRefs[i] ~= nil then 
			c = c + 1
			assert(baseObject.__index._object[objectRefs[i]] == objectRefs[i])
		else
			assert(baseObject.__index._object[objectRefs[i]] == nil)
		end
	end
	assert(baseObject.__indexCount._object == c)									-- check the object counts match



	-- Check the index counts are correct

	for index,_ in pairs(baseObject.__index) do 									-- work through each index
		c = 0
		for _,_ in pairs(baseObject.__index[index]) do c = c + 1 end 				-- count objects in index
		assert(baseObject.__indexCount[index] == c)									-- check matches the count.
	end
end

print("Completed.")