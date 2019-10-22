function printSkills(skills)
	for skillCount = 1, #skills do
		local skill = skills[skillCount]
		local skillName = skill[1]
		local skillMembers = skill[2]
		local texString = ""
		for skillMemberCount = 1, #skillMembers do
			local member = skillMembers[skillMemberCount]
			if member[2] == 1 then
				texString = texString .. member[1] .. "\\\\"
			end
		end
		tex.print("\\SkillEntry{"..skillName.."}{"..texString.."}")
	end 
end