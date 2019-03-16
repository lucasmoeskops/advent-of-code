import unittest
from operator import attrgetter

from main import Factory


class FactoryTestCase(unittest.TestCase):
    def test(self):
        deliveries = []
        factory = Factory()
        factory.on('delivery', lambda delivery: deliveries.append(delivery))
        instructions = [
            'value 5 goes to bot 2',
            'bot 2 gives low to bot 1 and high to bot 0',
            'value 3 goes to bot 1',
            'bot 1 gives low to output 1 and high to bot 0',
            'bot 0 gives low to output 2 and high to output 0',
            'value 2 goes to bot 2',
        ]
        factory.computer.parse_instructions(instructions)
        self.assertEqual(5, factory.bins[0].chips[0].value)
        self.assertEqual(2, factory.bins[1].chips[0].value)
        self.assertEqual(3, factory.bins[2].chips[0].value)
        self.assertIn((2, 5), [tuple(map(attrgetter('value'), delivery['chips']))
                               for delivery in deliveries
                               if delivery['bot_id'] == 2])


if __name__ == '__main__':
    unittest.main()
