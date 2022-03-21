

config_path = './config.ini'

f = open(config_path, 'r')
lines = f.readlines()
f.close()

print(lines[-1][19:])
print('---')