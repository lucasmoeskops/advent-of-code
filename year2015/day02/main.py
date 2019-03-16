lines = open('input.txt', 'r').read().strip().split('\n')
total = 0
for line in lines:
   args = list(map(int, line.split('x')))
   area = 2 * args[0] * args[1] + 2* args[1] * args[2] + 2 * args[2] * args[0]
   args.remove(max(args))
   total += area + args[0] * args[1]
print('The elves require {} square feet of wrapping.'.format(total))
total = 0
for line in lines:
   args = list(map(int, line.split('x')))
   cube = args[0] * args[1] * args[2]
   args.remove(max(args))
   total += cube + 2 * args[0] + 2 * args[1]
print('The elves require {} centimeter of ribbon.'.format(total))

