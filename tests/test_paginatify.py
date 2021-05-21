from paginatify import paginatify, NavigationBase


def paginate(count, page=1, base=NavigationBase.STANDARD):
    pagination = paginatify(
        range(1, count + 1), page=page, per_page=3, per_nav=3, base=base
    )
    assert pagination.total == count
    return pagination


def paginate_center(count, page=1):
    return paginate(count, page, NavigationBase.CENTER)


def test_normalize_page():
    assert paginate(0).page == 1

    # prevent overflow
    assert paginate(0, 2).page == 1

    # prevent underflow
    assert paginate(0, 0).page == 1


def test_last_page():
    assert paginate(0).last == 1

    assert paginate(1).last == 1
    assert paginate(2).last == 1
    assert paginate(3).last == 1

    assert paginate(4).last == 2
    assert paginate(5).last == 2
    assert paginate(6).last == 2


def test_nav_head():
    assert paginate(0).nav_head == 1

    assert paginate(31, 1).nav_head == 1
    assert paginate(31, 2).nav_head == 1
    assert paginate(31, 3).nav_head == 1

    assert paginate(31, 4).nav_head == 4
    assert paginate(31, 5).nav_head == 4
    assert paginate(31, 6).nav_head == 4

    assert paginate(31, 7).nav_head == 7
    assert paginate(31, 8).nav_head == 7
    assert paginate(31, 9).nav_head == 7

    assert paginate_center(0).nav_head == 1

    assert paginate_center(31, 1).nav_head == 1
    assert paginate_center(31, 2).nav_head == 1
    assert paginate_center(31, 3).nav_head == 2
    assert paginate_center(31, 4).nav_head == 3
    assert paginate_center(31, 5).nav_head == 4
    assert paginate_center(31, 6).nav_head == 5
    assert paginate_center(31, 7).nav_head == 6
    assert paginate_center(31, 8).nav_head == 7
    assert paginate_center(31, 9).nav_head == 8


def test_nav_tail():
    assert paginate(0).nav_tail == 1

    assert paginate(31, 1).nav_tail == 3
    assert paginate(31, 2).nav_tail == 3
    assert paginate(31, 3).nav_tail == 3

    assert paginate(31, 4).nav_tail == 6
    assert paginate(31, 5).nav_tail == 6
    assert paginate(31, 6).nav_tail == 6

    assert paginate(31, 7).nav_tail == 9
    assert paginate(31, 8).nav_tail == 9
    assert paginate(31, 9).nav_tail == 9

    assert paginate(31, 10).nav_tail == 11
    assert paginate(31, 11).nav_tail == 11
    p = paginate(31, 12)
    assert p.page == 11
    assert p.nav_tail == 11


    assert paginate_center(0).nav_tail == 1

    assert paginate_center(31, 1).nav_tail == 3
    assert paginate_center(31, 2).nav_tail == 3
    assert paginate_center(31, 3).nav_tail == 4

    assert paginate_center(31, 4).nav_tail == 5
    assert paginate_center(31, 5).nav_tail == 6
    assert paginate_center(31, 6).nav_tail == 7

    assert paginate_center(31, 7).nav_tail == 8
    assert paginate_center(31, 8).nav_tail == 9
    assert paginate_center(31, 9).nav_tail == 10

    assert paginate_center(31, 10).nav_tail == 11
    assert paginate_center(31, 11).nav_tail == 11
    p = paginate_center(31, 12)
    assert p.page == 11
    assert p.nav_tail == 11


def test_pages():
    assert paginate(0).pages == (1,)

    assert paginate(31, 1).pages == (1, 2, 3)
    assert paginate(31, 2).pages == (1, 2, 3)
    assert paginate(31, 3).pages == (1, 2, 3)

    assert paginate(31, 4).pages == (4, 5, 6)
    assert paginate(31, 5).pages == (4, 5, 6)
    assert paginate(31, 6).pages == (4, 5, 6)

    assert paginate(31, 7).pages == (7, 8, 9)
    assert paginate(31, 8).pages == (7, 8, 9)
    assert paginate(31, 9).pages == (7, 8, 9)

    assert paginate(31, 10).pages == (10, 11)
    assert paginate(31, 11).pages == (10, 11)
    assert paginate(31, 12).pages == (10, 11)


def test_items():
    assert paginate(0).items == ()

    assert paginate(31, 1).items == (1, 2, 3)
    assert paginate(31, 2).items == (4, 5, 6)
    assert paginate(31, 3).items == (7, 8, 9)

    assert paginate(31, 10).items == (28, 29, 30)
    assert paginate(31, 11).items == (31,)
    assert paginate(31, 12).items == (31,)


def test_first():
    assert paginate(0).first == 1


def test_prev():
    assert paginate(0).prev == 1


def test_has_prev():
    assert paginate(0).has_prev is False
    assert paginate(4, 2).has_prev is True


def test_next():
    assert paginate(0).next == 1


def test_has_next():
    assert paginate(0).has_next is False
    assert paginate(4).has_next is True
    assert paginate(4, 2).has_next is False


def test_nav_prev():
    assert paginate(0).nav_prev == 1


def test_has_nav_prev():
    assert paginate(0).has_nav_prev is False
    assert paginate(10, 1).has_nav_prev is False
    assert paginate(10, 4).has_nav_prev is True


def test_nav_next():
    assert paginate(0).nav_next == 1


def test_has_nav_next():
    assert paginate(0).has_nav_next is False
    assert paginate(10).has_nav_next is True
    assert paginate(10, 4).has_nav_next is False


def test_items_indexed():
    assert paginate(0).items_indexed == ()

    assert paginate(1).items_indexed == ((1, 1),)
    assert paginate(2).items_indexed == ((2, 1), (1, 2))
    assert paginate(3).items_indexed == ((3, 1), (2, 2), (1, 3))
    assert paginate(4).items_indexed == ((4, 1), (3, 2), (2, 3))
    assert paginate(4, 2).items_indexed == ((1, 4),)

    assert paginate(31, 1).items_indexed == ((31, 1), (30, 2), (29, 3))
    assert paginate(31, 2).items_indexed == ((28, 4), (27, 5), (26, 6))
    assert paginate(31, 3).items_indexed == ((25, 7), (24, 8), (23, 9))

    assert paginate(31, 10).items_indexed == ((4, 28), (3, 29), (2, 30))
    assert paginate(31, 11).items_indexed == ((1, 31),)
    assert paginate(31, 12).items_indexed == ((1, 31),)
