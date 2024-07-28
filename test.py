trap_name='2E_MCP'
Vinlet=10.0
Vfloor=2
Voutlet=10
handle_name='handle'

unique_key1 = handle_name + "_" + trap_name + str(Vinlet) + str(Vfloor) + str(Voutlet)
print(unique_key1)

trap_name='2E_MCP'
Vinlet=1
Vfloor=0.02
Voutlet=10
handle_name='handle'

unique_key2 = handle_name + "_" + trap_name + str(Vinlet) + str(Vfloor) + str(Voutlet)
print(unique_key2)

print(f'Same={unique_key1==unique_key2}')