import unittest
import yaml
from frequency_mapper import get_frequency

class TestFrequencyMapper(unittest.TestCase):
    def setUp(self):
        # Mock frequency data as it would be loaded from frequencies.yaml
        self.mock_frequencies = {
            'Hero': {
                'base': 396,
                'modifiers': ['courage', 'risk']
            },
            'Lover': {
                'base': 528,
                'modifiers': ['connection', 'beauty']
            },
            'Outlaw': {
                'base': 741,
                'modifiers': ['chaos', 'rejection']
            }
        }

    def test_valid_archetype(self):
        freq = get_frequency('Hero', self.mock_frequencies)
        self.assertEqual(freq, 396)

    def test_another_archetype(self):
        freq = get_frequency('Lover', self.mock_frequencies)
        self.assertEqual(freq, 528)

    def test_invalid_archetype(self):
        with self.assertRaises(KeyError):
            get_frequency('Jester', self.mock_frequencies)

    def test_yaml_structure(self):
        # Simulate loading from a .yaml string
        yaml_content = """
        Sage:
          base: 963
          modifiers:
            - awareness
            - knowledge
        """
        frequencies = yaml.safe_load(yaml_content)
        self.assertIn('Sage', frequencies)
        self.assertEqual(frequencies['Sage']['base'], 963)

if __name__ == '__main__':
    unittest.main()
