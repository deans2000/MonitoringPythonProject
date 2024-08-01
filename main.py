from Poarta1 import *

# Creating instances
Dean = Poarta1(1, 'in')
Mihai = Poarta1(2, 'in')
Dean2 = Poarta1(1, 'out')
Mihai2 = Poarta1(2, 'out')

# Collecting entries
Dean.salvareDate()
Mihai.salvareDate()
Dean2.salvareDate()
Mihai2.salvareDate()

# Save all entries to files
Poarta1.save_all_entries()
