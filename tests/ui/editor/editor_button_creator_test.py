from aqt.editor import Editor

from cross_field_highlighter.ui.editor.editor_button_creator import EditorButtonCreator


def test_create_highlight_button(editor_button_creator: EditorButtonCreator, editor_edit_mode: Editor,
                                 editor_add_mode: Editor):
    exp: str = """<button tabindex=-1
                        
                        class="linkb"
                        type="button"
                        title="Open Highlight dialog for current note...\n(Cross-Field Highlighter)\nCtrl+Shift+H"
                        onclick="pycmd('highlight_button_cmd');return false;"
                        onmousedown="window.event.preventDefault();"
                >
                    <img class="topbut" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAeCAMAAAB61OwbAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAtNQTFRFAAAAZkhIZkdHZUhIcEtLZklJhEdHZktLZkhIZkhIZkhIZkhIZkhIZkhIZkhIZkhIZkhIZUdIZkhIZkhIZkhIZUdIZkhIZkhIZEdHZkhIZkhIZkhIZEdHZkhIZkhIZkhIZkhIZEdHZkhIZ0hIZkhIZUhIZUdIZkhIZkhIZkhIZkhIZUhIZkdHZkhIZUhIZUdIZkhIZkhIZklJZkhIZUhIZkhIZ0lJZUhIZkhIZkhIZkhIZUhIZkhIZkhIZkhIZkhIZkhIZkhIZkhIZkhIZkhIZkhIZkhIZkhIZkhIZkhIZkhIZkhIZkdHZkhIZkhIZkhIZkhIZkhIZkhIZkhIZUhIZkhIZkdHZUZGZkhIZkhIZ0dHZkhIZkhIZkhIZUZFZUdGZkhHZkhIZkdHZUZGZkhIZkhIZkhIZkhIZkhIa01KrYpivplodldOZEdHa0xKtZFl+9N//9eB0apvdlZOaEpJs49k+9J//9aA/9WAq4hh+NB+0KpvdVZOZ0lJqodhz6lvZ0lIqYZg+M9+/9aByaNsbE1KqIVg989+2rNzcFFM47x2hGRTZUdI5b53h2ZUZEZH5r53iGhVp4Rg6sJ5jGtW98996sN5j21XZUdHpoNf7MR5j25XoH5d9cx97sZ6knBYb1BL1rBx/9iB78d6lHNZZklJaVFThGNT4bp1ZkdGdXV/jLbPcWhwY0RFg2NT4rt2gZanm+H/kMPecWduhWRTbV1ikMPfmuD/cGZthmVU5L12ZUZGgZepmt//kMLdcGRrZERFh2dU8cl7l3VaZUVFfYqamd7/md3/j8HcZEVFiWhV57938sl7mXdbZ0tMiKzDcGRqZklKfImYl9j4ldHwk8vpl9f3kMHcZ0xNhqW5mNv7hKC1b2NpbFlddXR+jrzWlNDvdneBakxKbExJa1dbeHyIaE5Qa1dab2JoZ0pKk3JY2LFynHpcZ0hHcVJMclNM////SCz5SgAAAGh0Uk5TAAAAAAAAAAAFZsrUjBgEbfL9qxlu8qcW/qWkEv2YDwNs/JUDaPH6kAJl7+8DZO74X7cBVukuAejML0/nzjBO5DHQM03f0TWC2DbcQ/tEsuJHi+NMAVfqAVTnAVJe5fPM8m/X4UIXHgvDFOrkAAAAAWJLR0TwNbjvVAAAAAlwSFlzAAD9RwAA/UcB/7VOKAAAAexJREFUKM9jYMAEjBycXNw8vIwMOAAjH79ARoagkDAjLnkR0cys7JxcMXFGXPJ5+QWFRcUSkthUgORLSsvKK8qBKqSkGbHKV1aVV1RUlFfXyMjKoalglFeAyYNVKCrJocorq6jW1kHlgSrqa9TUUeQ1NLUaGptg8hUVzS2t2sjyOrp6DW3tCPmKwo5OfWT9BujyXd09hgh5I2MTNPnevn4uU7i8mbE5mvyEif0WljBvMjJZWTdMQpGfPKXfxpYRqoCZxc6+YdJUZPlp02fYOMDkGRnt7DNmouifNTsXVb52zlxk+XnzZzg6IeSd7WcsWLgIId+8eEkPQp6B0cFl6bIZy1cUIsu7usHlGRjdV65avWbtuvWFCHkPT4Q8A6PSyg0bN21eu6WrECbv5Y0kz8Co6bN12/ZNO9bu3FUIlfdlRU4HjHJ+u/fs3btv/4GDEwqbDx2e4R/AxIoSy2yBR44eO773xP6Tp06fOdsTFMyIko4YQ0LDzp3fe+zY3hMXDkw5nBEUjGI+A1N4ROTFS5ePXbl6bfv1/bt77J3ZUdNhVHRk/42bt27fuXvv/oOHu+2dGdHSaUzso52Pnzx9Fhcf9/zFyyAMeYbInlev37zdnZAoJ5KUbJiCIc+glfGu5n2DAD8fo0ZqWjqmPACY5/c633BZnQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxOC0wMy0yN1QxMTo1MDo1MiswMjowMA0R1KMAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTgtMDMtMjdUMTE6NTA6NTIrMDI6MDB8TGwfAAAARnRFWHRzb2Z0d2FyZQBJbWFnZU1hZ2ljayA2LjcuOC05IDIwMTYtMDYtMTYgUTE2IGh0dHA6Ly93d3cuaW1hZ2VtYWdpY2sub3Jn5r80tgAAABh0RVh0VGh1bWI6OkRvY3VtZW50OjpQYWdlcwAxp/+7LwAAABh0RVh0VGh1bWI6OkltYWdlOjpoZWlnaHQANTEywNBQUQAAABd0RVh0VGh1bWI6OkltYWdlOjpXaWR0aAA1MzdeIJXRAAAAGXRFWHRUaHVtYjo6TWltZXR5cGUAaW1hZ2UvcG5nP7JWTgAAABd0RVh0VGh1bWI6Ok1UaW1lADE1MjIxNDQyNTLPe/bHAAAAEXRFWHRUaHVtYjo6U2l6ZQAxOEtCQh7deOoAAAA/dEVYdFRodW1iOjpVUkkAZmlsZTovLy4vdXBsb2Fkcy81Ni9SSldPMFZpLzEzOTMvaGlnaGxpZ2h0Xzk2NzI5LnBuZ3bxVfYAAAAASUVORK5CYII=">
                    
                </button>"""
    assert editor_button_creator.create_highlight_button(editor_edit_mode) == exp
    assert editor_button_creator.create_highlight_button(editor_add_mode) == exp


def test_create_erase_button(editor_button_creator: EditorButtonCreator, editor_edit_mode: Editor,
                             editor_add_mode: Editor):
    exp: str = """<button tabindex=-1
                        
                        class="linkb"
                        type="button"
                        title="Open Erase dialog for current note...\n(Cross-Field Highlighter)\nCtrl+Shift+E"
                        onclick="pycmd('erase_button_cmd');return false;"
                        onmousedown="window.event.preventDefault();"
                >
                    <img class="topbut" src="data:image/png;base64,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">
                    
                </button>"""
    assert editor_button_creator.create_erase_button(editor_edit_mode) == exp
    assert editor_button_creator.create_erase_button(editor_add_mode) == exp
