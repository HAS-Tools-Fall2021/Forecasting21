# %% 
import sys
sys.path.insert(1, '../')
import eval_functions as ef

weeknum = 1

all_names = ef.getFirstNames()
print(all_names)

#picking based on who submitted first
bonus_pick = [4, 6, 7]

#Extract the names from the picked values
bonus_names = [all_names[i] for i in bonus_pick]
print(bonus_names)

#Write out the bonus points
ef.write_bonus(bonus_names, all_names, weeknum)

# %%
