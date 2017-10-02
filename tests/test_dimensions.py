from unittest import TestCase

from .utils import TestNode


class SizeTests(TestCase):
    def setUp(self):
        self.node = TestNode()
        # Mark the layout as "in calculation"
        self.node.layout.dirty = None

    def assertSize(self, size, values):
        self.assertEqual(values[0], size.width)
        self.assertEqual(values[1], size.height)
        self.assertEqual(values[2], size.exact_width)
        self.assertEqual(values[3], size.exact_height)
        self.assertEqual(values[4], size.ratio)
        self.assertEqual(values[5], size.is_replaced)

    def test_initial_state(self):
        self.assertSize(self.node.intrinsic, (None, None, True, True, None, False))

        # Layout has not been touched.
        self.assertIsNone(self.node.layout.dirty)

    def test_set_width(self):
        self.node.intrinsic.width = 10
        self.assertSize(self.node.intrinsic, (10, None, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the width to the same value
        self.node.intrinsic.width = 10
        self.assertSize(self.node.intrinsic, (10, None, True, True, None, False))

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the width to something new
        self.node.intrinsic.width = 20
        self.assertSize(self.node.intrinsic, (20, None, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

    def test_set_height(self):
        self.node.intrinsic.height = 10
        self.assertSize(self.node.intrinsic, (None, 10, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the height to the same value
        self.node.intrinsic.height = 10
        self.assertSize(self.node.intrinsic, (None, 10, True, True, None, False))

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the height to something new
        self.node.intrinsic.height = 20
        self.assertSize(self.node.intrinsic, (None, 20, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

    def test_set_exact_width(self):
        self.node.intrinsic.exact_width = False
        self.assertSize(self.node.intrinsic, (None, None, False, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the exact_width to the same value
        self.node.intrinsic.exact_width = False
        self.assertSize(self.node.intrinsic, (None, None, False, True, None, False))

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the exact_width to something new
        self.node.intrinsic.exact_width = True
        self.assertSize(self.node.intrinsic, (None, None, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

    def test_set_exact_height(self):
        self.node.intrinsic.exact_height = False
        self.assertSize(self.node.intrinsic, (None, None, True, False, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the exact height to the same value
        self.node.intrinsic.exact_height = False
        self.assertSize(self.node.intrinsic, (None, None, True, False, None, False))

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the exact height to something else
        self.node.intrinsic.exact_height = True
        self.assertSize(self.node.intrinsic, (None, None, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

    def test_set_ratio(self):
        self.node.intrinsic.ratio = 0.5
        self.assertSize(self.node.intrinsic, (None, None, True, True, 0.5, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set the ratio to the same value
        self.node.intrinsic.ratio = 0.5
        self.assertSize(self.node.intrinsic, (None, None, True, True, 0.5, False))

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set the ratio to something else
        self.node.intrinsic.ratio = 0.75
        self.assertSize(self.node.intrinsic, (None, None, True, True, 0.75, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

    def test_set_is_replaced(self):
        self.node.intrinsic.is_replaced = True
        self.assertSize(self.node.intrinsic, (None, None, True, True, None, True))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)

        # Clean the layout
        self.node.layout.dirty = False

        # Set is_replaced to the same value
        self.node.intrinsic.is_replaced = True
        self.assertSize(self.node.intrinsic, (None, None, True, True, None, True))

        # Layout has NOT been dirtied.
        self.assertFalse(self.node.intrinsic.dirty)

        # Set is_replaced to something else
        self.node.intrinsic.is_replaced = False
        self.assertSize(self.node.intrinsic, (None, None, True, True, None, False))

        # Layout has been dirtied.
        self.assertTrue(self.node.intrinsic.dirty)


class BoxTests(TestCase):
    def setUp(self):
        self.node = TestNode()
        self.node.layout.content_width = 10
        self.node.layout.content_height = 16

        self.child1 = TestNode()
        self.child1.layout.content_width = 10
        self.child1.layout.content_height = 16
        self.child2 = TestNode()

        self.grandchild1_1 = TestNode()
        self.grandchild1_1.layout.content_width = 10
        self.grandchild1_1.layout.content_height = 16
        self.grandchild1_2 = TestNode()

        self.node.children = [self.child1, self.child2]
        self.child1.children = [self.grandchild1_1, self.grandchild1_2]

        # Mark the layout as "in calculation"
        self.node.layout.dirty = None

    def assertLayout(self, box, expected):
        actual = {}
        if 'origin' in expected:
            actual['origin'] = (box.origin_left, box.origin_top)

        if 'size' in expected:
            actual['size'] = {}
            if 'margin' in expected['size']:
                actual['size']['margin'] = (box.margin_box_width, box.margin_box_height)

            if 'border' in expected['size']:
                actual['size']['border'] = (box.border_box_width, box.border_box_height)

            if 'padding' in expected['size']:
                actual['size']['padding'] = (box.padding_box_width, box.padding_box_height)

            if 'content' in expected['size']:
                actual['size']['content'] = (box.content_width, box.content_height)

        if 'relative' in expected:
            actual['relative'] = {}
            if 'margin' in expected['relative']:
                actual['relative']['margin'] = (
                    box.margin_box_top,
                    box.margin_box_right,
                    box.margin_box_bottom,
                    box.margin_box_left,
                )

            if 'border' in expected['relative']:
                actual['relative']['border'] = (
                    box.border_box_top,
                    box.border_box_right,
                    box.border_box_bottom,
                    box.border_box_left,
                )

            if 'padding' in expected['relative']:
                actual['relative']['padding'] = (
                    box.padding_box_top,
                    box.padding_box_right,
                    box.padding_box_bottom,
                    box.padding_box_left,
                )

            if 'content' in expected['relative']:
                actual['relative']['content'] = (
                    box.content_top,
                    box.content_right,
                    box.content_bottom,
                    box.content_left,
                )

        if 'absolute' in expected:
            actual['absolute'] = {}
            if 'margin' in expected['absolute']:
                actual['absolute']['margin'] = (
                    box.absolute_margin_top,
                    box.absolute_margin_right,
                    box.absolute_margin_bottom,
                    box.absolute_margin_left,
                )

            if 'border' in expected['absolute']:
                actual['absolute']['border'] = (
                    box.absolute_border_top,
                    box.absolute_border_right,
                    box.absolute_border_bottom,
                    box.absolute_border_left,
                )

            if 'padding' in expected['absolute']:
                actual['absolute']['padding'] = (
                    box.absolute_padding_top,
                    box.absolute_padding_right,
                    box.absolute_padding_bottom,
                    box.absolute_padding_left,
                )

            if 'content' in expected['absolute']:
                actual['absolute']['content'] = (
                    box.absolute_content_top,
                    box.absolute_content_right,
                    box.absolute_content_bottom,
                    box.absolute_content_left,
                )

        self.assertEqual(actual, expected)

    def assertDirty(self, n, c1, c2, gc1, gc2):
        self.assertEqual(n, self.node.layout.dirty)
        self.assertEqual(c1, self.child1.layout.dirty)
        self.assertEqual(c2, self.child2.layout.dirty)
        self.assertEqual(gc1, self.grandchild1_1.layout.dirty)
        self.assertEqual(gc2, self.grandchild1_2.layout.dirty)

    def test_initial(self):
        # Core attributes have been stored
        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {
                    'content': (10, 16),
                    'padding': (10, 16),
                    'border': (10, 16),
                    'margin': (10, 16),
                },
                'relative': {
                    'content': (0, 10, 16, 0),
                    'padding': (0, 10, 16, 0),
                    'border': (0, 10, 16, 0),
                    'margin': (0, 10, 16, 0),
                },
                'absolute': {
                    'content': (0, 10, 16, 0),
                    'padding': (0, 10, 16, 0),
                    'border': (0, 10, 16, 0),
                    'margin': (0, 10, 16, 0),
                }
            }
        )

        # All the nodes are in calcuation
        self.assertDirty(None, None, None, None, None)

    def test_set_top(self):
        self.node.layout.content_top = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (5, 10, 21, 0)},
                'absolute': {'content': (5, 10, 21, 0)},
            }
        )

        # All the nodes have been marked dirty
        self.assertDirty(True, True, True, True, True)

        # Set the layout back to calculation
        self.node.layout.dirty = None

        # Set the top to the same value
        self.node.layout.content_top = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (5, 10, 21, 0)},
                'absolute': {'content': (5, 10, 21, 0)},
            }
        )

        # Dirty state has not changed.
        self.assertDirty(None, None, None, None, None)

        # Set the top to a new value
        self.node.layout.content_top = 7

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (7, 10, 23, 0)},
                'absolute': {'content': (7, 10, 23, 0)},
            }
        )

        # All the nodes have been marked dirty
        self.assertDirty(True, True, True, True, True)

    def test_set_left(self):
        self.node.layout.content_left = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (0, 15, 16, 5)},
                'absolute': {'content': (0, 15, 16, 5)},
            }
        )

        # All the nodes have been marked dirty
        self.assertDirty(True, True, True, True, True)

        # Set the layout back to calculation
        self.node.layout.dirty = None

        # Set the left to the same value
        self.node.layout.content_left = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (0, 15, 16, 5)},
                'absolute': {'content': (0, 15, 16, 5)},
            }
        )

        # Dirty state has not changed.
        self.assertDirty(None, None, None, None, None)

        # Set the left to a new value
        self.node.layout.content_left = 7

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (0, 17, 16, 7)},
                'absolute': {'content': (0, 17, 16, 7)},
            }
        )

        # All the nodes have been marked dirty
        self.assertDirty(True, True, True, True, True)

    def test_set_height(self):
        self.node.layout.content_height = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 5)},
                'relative': {'content': (0, 10, 5, 0)},
                'absolute': {'content': (0, 10, 5, 0)},
            }
        )

        # All the nodes have been marked dirty
        self.assertDirty(True, True, True, True, True)

        # Set the layout back to calculation
        self.node.layout.dirty = None

        # Set the height to the same value
        self.node.layout.content_height = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 5)},
                'relative': {'content': (0, 10, 5, 0)},
                'absolute': {'content': (0, 10, 5, 0)},
            }
        )

        # Dirty state has not changed.
        self.assertDirty(None, None, None, None, None)

        # Set the height to a new value
        self.node.layout.content_height = 7

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (10, 7)},
                'relative': {'content': (0, 10, 7, 0)},
                'absolute': {'content': (0, 10, 7, 0)},
            }
        )

        # All the nodes have been marked dirty
        self.assertDirty(True, True, True, True, True)

    def test_set_width(self):
        self.node.layout.content_width = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (5, 16)},
                'relative': {'content': (0, 5, 16, 0)},
                'absolute': {'content': (0, 5, 16, 0)},
            }
        )

        # All the nodes have been marked dirty
        self.assertDirty(True, True, True, True, True)

        # Set the layout back to calculation
        self.node.layout.dirty = None

        # Set the width to the same value
        self.node.layout.content_width = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (5, 16)},
                'relative': {'content': (0, 5, 16, 0)},
                'absolute': {'content': (0, 5, 16, 0)},
            }
        )

        # Dirty state has not changed.
        self.assertDirty(None, None, None, None, None)

        # Set the width to a new value
        self.node.layout.content_width = 7

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 0),
                'size': {'content': (7, 16)},
                'relative': {'content': (0, 7, 16, 0)},
                'absolute': {'content': (0, 7, 16, 0)},
            }
        )

        # All the nodes have been marked dirty
        self.assertDirty(True, True, True, True, True)

    def test_set_origin_top(self):
        self.node.layout.origin_top = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 5),
                'size': {'content': (10, 16)},
                'relative': {'content': (0, 10, 16, 0)},
                'absolute': {'content': (5, 10, 21, 0)},
            }
        )

        # All the nodes have been marked dirty
        self.assertDirty(True, True, True, True, True)

        # Set the layout back to calculation
        self.node.layout.dirty = None

        # Set the origin_top to the same value
        self.node.layout.origin_top = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 5),
                'size': {'content': (10, 16)},
                'relative': {'content': (0, 10, 16, 0)},
                'absolute': {'content': (5, 10, 21, 0)},
            }
        )

        # Dirty state has not changed.
        self.assertDirty(None, None, None, None, None)

        # Set the origin_top to a new value
        self.node.layout.origin_top = 7

        self.assertLayout(
            self.node.layout,
            {
                'origin': (0, 7),
                'size': {'content': (10, 16)},
                'relative': {'content': (0, 10, 16, 0)},
                'absolute': {'content': (7, 10, 23, 0)},
            }
        )

        # All the nodes have been marked dirty
        self.assertDirty(True, True, True, True, True)

    def test_set_origin_left(self):
        self.node.layout.origin_left = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (5, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (0, 10, 16, 0)},
                'absolute': {'content': (0, 15, 16, 5)},
            }
        )

        # All the nodes have been marked dirty
        self.assertDirty(True, True, True, True, True)

        # Set the layout back to calculation
        self.node.layout.dirty = None

        # Set the origin_left to the same value
        self.node.layout.origin_left = 5

        self.assertLayout(
            self.node.layout,
            {
                'origin': (5, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (0, 10, 16, 0)},
                'absolute': {'content': (0, 15, 16, 5)},
            }
        )

        # Dirty state has not changed.
        self.assertDirty(None, None, None, None, None)

        # Set the origin_left to a new value
        self.node.layout.origin_left = 7

        self.assertLayout(
            self.node.layout,
            {
                'origin': (7, 0),
                'size': {'content': (10, 16)},
                'relative': {'content': (0, 10, 16, 0)},
                'absolute': {'content': (0, 17, 16, 7)},
            }
        )

        # All the nodes have been marked dirty
        self.assertDirty(True, True, True, True, True)

    def test_descendent_offsets(self):
        self.node.layout.origin_top = 5
        self.node.layout.origin_left = 6

        self.node.layout.content_top = 7
        self.node.layout.content_left = 8

        self.child1.layout.content_top = 9
        self.child1.layout.content_left = 10

        self.grandchild1_1.layout.content_top = 11
        self.grandchild1_1.layout.content_left = 12

        self.assertLayout(
            self.node.layout,
            {
                'origin': (6, 5),
                'size': {'content': (10, 16)},
                'relative': {'content': (7, 18, 23, 8)},
                'absolute': {'content': (12, 24, 28, 14)},
            }
        )

        self.assertLayout(
            self.child1.layout,
            {
                'origin': (14, 12),
                'size': {'content': (10, 16)},
                'relative': {'content': (9, 20, 25, 10)},
                'absolute': {'content': (21, 34, 37, 24)},
            }
        )

        self.assertLayout(
            self.grandchild1_1.layout,
            {
                'origin': (24, 21),
                'size': {'content': (10, 16)},
                'relative': {'content': (11, 22, 27, 12)},
                'absolute': {'content': (32, 46, 48, 36)},
            }
        )

        # All the nodes have been marked dirty
        self.assertDirty(True, True, True, True, True)

        # Clean the layout
        self.node.layout.dirty = False

        # Modify the grandchild position
        self.grandchild1_1.layout.content_top = 13
        self.grandchild1_1.layout.content_left = 14

        # Only the grandchild position has changed.
        self.assertLayout(
            self.node.layout,
            {
                'origin': (6, 5),
                'size': {'content': (10, 16)},
                'relative': {'content': (7, 18, 23, 8)},
                'absolute': {'content': (12, 24, 28, 14)},
            }
        )

        self.assertLayout(
            self.child1.layout,
            {
                'origin': (14, 12),
                'size': {'content': (10, 16)},
                'relative': {'content': (9, 20, 25, 10)},
                'absolute': {'content': (21, 34, 37, 24)},
            }
        )

        self.assertLayout(
            self.grandchild1_1.layout,
            {
                'origin': (24, 21),
                'size': {'content': (10, 16)},
                'relative': {'content': (13, 24, 29, 14)},
                'absolute': {'content': (34, 48, 50, 38)},
            }
        )

        # Only the grandchild node is dirty
        self.assertDirty(False, False, False, True, False)

        # Modify the child position
        self.child1.layout.content_top = 15
        self.child1.layout.content_left = 16

        # The child and grandchild position has changed.
        self.assertLayout(
            self.node.layout,
            {
                'origin': (6, 5),
                'size': {'content': (10, 16)},
                'relative': {'content': (7, 18, 23, 8)},
                'absolute': {'content': (12, 24, 28, 14)},
            }
        )

        self.assertLayout(
            self.child1.layout,
            {
                'origin': (14, 12),
                'size': {'content': (10, 16)},
                'relative': {'content': (15, 26, 31, 16)},
                'absolute': {'content': (27, 40, 43, 30)},
            }
        )

        self.assertLayout(
            self.grandchild1_1.layout,
            {
                'origin': (30, 27),
                'size': {'content': (10, 16)},
                'relative': {'content': (13, 24, 29, 14)},
                'absolute': {'content': (40, 54, 56, 44)},
            }
        )

        # Only the affected child node, and grandchild nodes are dirty
        self.assertDirty(False, True, False, True, True)
