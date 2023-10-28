import pytest


@pytest.fixture()
def sample_openai_response():
    return \
    {
        'id': 'chatcmpl-8DjQeT87pA8PlK0dER8JVUJKRJWQz',
        'object': 'chat.completion',
        'created': 1698283584,
        'model': 'gpt-3.5-turbo-0613',
        'choices': [
            {'index': 0,
             'message':
                 {
                    'role': 'assistant',
                    'content': '[{"image_path": "test_path/image1.png", "image_caption": "a child pulls on a tablecloth", "story": "Once upon a time, there was a mischievous child who loved to explore new adventures. In one of his escapades, he found himself in a grand dining hall filled with delicious food and delicate china plates. Intrigued by the sight, the child couldn\'t resist the temptation to unravel a magical trick he had seen in a circus show. With a mischievous grin, he tiptoed towards the table and grabbed hold of the crisp white tablecloth with all his might. He was determined to pull it off in one smooth motion, just like the performers did at the circus."}, '
                             '{"image_path": "other_test_path/image2.png", "image_caption": "a child starts to pull a tablecloth off of the table", "story": "As the child tugged on the tablecloth, he could feel the resistance beneath it. The plates and cutlery on the table wobbled slightly, sending shivers of excitement down the child\'s spine. With each pull, the child\'s confidence grew, and he imagined himself as the star of his own daring act. The room was filled with anticipation as the child\'s tiny hands continued to yank on the cloth, drawing closer to the ultimate moment of truth."}, '
                             '{"image_path": "other_other_test_path/image2.png", "image_caption": "a child covered in food in front of a table with food on the floor", "story": "But alas, all good plans come with unexpected outcomes. The child\'s ambitious endeavor had led to a cascade of events that he could not have foreseen. With one final tug, the tablecloth slipped out from under the dishes, causing them to crash dramatically onto the floor. A symphony of clattering sounds filled the air as food tumbled off the plates, splattering in all directions. And right in the middle of the chaos stood the child, covered from head to toe in a colorful mess. Despite the accidental disaster, the child couldn\'t help but burst into laughter, realizing that sometimes the most memorable adventures come from the unexpected."}]'
                  },
             'finish_reason': 'stop'}
        ],
        'usage': {
            'prompt_tokens': 251,
            'completion_tokens': 445,
            'total_tokens': 696
        }
    }