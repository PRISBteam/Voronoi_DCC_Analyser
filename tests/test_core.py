import matplotlib.pyplot as plt
import pytest

from matgen import core

def test_create_ax():
    """
    """
    ax = core._create_ax()
    plt.savefig('tests/figures/new-ax-default.png')

    ax = core._create_ax(dim=3)
    plt.savefig('tests/figures/new-ax-3D.png')

    ax = core._create_ax(dim=2, figsize=(16,16))
    plt.savefig('tests/figures/new-ax-2D-size-16.png')

    ax = core._create_ax(dim=3, figsize=(4,4))
    plt.savefig('tests/figures/new-ax-3D-size-4.png')


def test_Vertex():
    """
    """
    v = core.Vertex(id=42, x=0.34, y=0.58, z=0.89)
    assert v.id == 42, f"Vertex id {v.id} doesn't match 42"
    assert v.x == pytest.approx(0.34)
    assert v.y == pytest.approx(0.58)
    assert v.z == pytest.approx(0.89)
    assert v.coord == pytest.approx((0.34, 0.58, 0.89))
    assert v.coord2D == pytest.approx((0.34, 0.58))
    assert v.__str__() == "Vertex(id=42)"


def test_Vertex_add_neighbors():
    """
    """
    v = core.Vertex(id=42, x=0.34, y=0.58, z=0.89)
    v.add_neighbor(21)
    v.add_neighbor(34)
    v.add_neighbors([1, 2])
    v.add_neighbors([5, 1, 3])
    v.add_neighbor(2)
    assert set(v.neighbor_ids) == {1, 2, 3, 5, 21, 34}
    assert len(v.neighbor_ids) == 6


def test_Vertex_add_incident():
    """
    """
    v = core.Vertex(id=42, x=0.34, y=0.58, z=0.89)
    v.add_incident_edge(21)
    v.add_incident_edge(34)
    v.add_incident_edges([1, 2])
    v.add_incident_edges([5, 1, 3])
    v.add_incident_edge(5)
    assert len(v.e_ids) == 6
    assert v.get_degree() == 6
    assert len(v.incident_cells) == 6
    assert set(v.e_ids) == {1, 2, 3, 5, 21, 34}
    assert set(v.incident_cells) == {1, 2, 3, 5, 21, 34}


def test_Vertex_set():
    """
    """
    v = core.Vertex(id=42, x=0.34, y=0.58, z=0.89)
    assert not v.is_external
    v.set_external(True)
    assert v.is_external
    v.set_external(False)
    assert not v.is_external
    
    v.set_junction_type('E')
    assert v.junction_type == 'E'
    v.set_junction_type('J1')
    assert v.junction_type == 'J1'


def test_Vertex_plot():
    """
    """
    points = [
        (0.0, 0.0),
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, 0.0),
        (1.0, 0.0)
    ]
    ax = core.Vertex(id=21, x=0.5, y=0.5).plot(dim=2, color='k', label=21)
    i = 0
    for x, y in points:
        i += 1
        v = core.Vertex(id=i, x=x, y=y)
        ax = v.plot(dim=2, ax=ax, label=i)
    ax.legend(loc='best')
    plt.savefig('tests/figures/vertices-2D-6.png')

    points = [
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 1.0),
        (0.0, 1.0, 0.0),
        (0.0, 1.0, 1.0),
        (1.0, 0.0, 0.0),
        (1.0, 0.0, 1.0),
        (1.0, 1.0, 0.0),
        (1.0, 1.0, 1.0)
    ]
    ax = core.Vertex(id=21, x=0.5, y=0.5, z=0.5).plot(
        dim=3, color='k', label=21
    )
    i = 0
    for x, y, z in points:
        i += 1
        v = core.Vertex(id=i, x=x, y=y, z=z)
        ax = v.plot(dim=3, ax=ax, label=i)
    ax.legend(loc='best')
    plt.savefig('tests/figures/vertices-3D-9.png')

    ax = core.Vertex(id=21, x=0.5, y=0.5, z=0.5).plot(
        dim=2, color='r', label=22
    )
    ax.legend(loc='best')
    plt.savefig('tests/figures/vertices-2D-1.png')


def test_Vertex_from_tess_file():
    """
    """
    filename = 'tests/test_data/n8-id1.tess'
    _vertices = core.Vertex.from_tess_file(filename)
    assert len(_vertices.keys()) == 41
    assert _vertices[20].z == pytest.approx(0.581244510538)
    assert _vertices[33].y == pytest.approx(0.377184567183)
    assert _vertices[39].x == pytest.approx(0.658946058940)

    ax = core._create_ax(dim=3)

    for v in _vertices.values():
        if v.x in [0.0, 1.0] or v.y in [0.0, 1.0] or v.z in [0.0, 1.0]:
            ax = v.plot(dim=3, ax=ax, color='b')
        else:
            ax = v.plot(dim=3, ax=ax, color='r')
    plt.savefig('tests/figures/vertices-3D-41.png')


def test_Edge():
    """
    """
    e = core.Edge(id=42, v_ids=[5, 1])
    assert e.id == 42
    assert len(e.v_ids) == 2
    assert e.v_ids == [5, 1]
    assert e.__str__() == "Edge(id=42)"


def test_Edge_add_neighbors():
    """
    """
    e = core.Edge(id=42, v_ids=[5, 1])
    e.add_neighbor(21)
    e.add_neighbor(34)
    e.add_neighbors([1, 2])
    e.add_neighbors([5, 1, 3])
    e.add_neighbor(2)
    assert len(e.neighbor_ids) == 6
    assert set(e.neighbor_ids) == {1, 2, 3, 5, 21, 34}


def test_Edge_add_incident():
    """
    """
    e = core.Edge(id=42, v_ids=[5, 1])
    e.add_incident_face(21)
    e.add_incident_face(34)
    e.add_incident_faces([1, 2])
    e.add_incident_faces([5, 1, 3])
    e.add_incident_face(5)
    assert len(e.f_ids) == 6
    assert e.get_degree() == 6
    assert len(e.incident_cells) == 6
    assert set(e.f_ids) == {1, 2, 3, 5, 21, 34}
    assert set(e.incident_cells) == {1, 2, 3, 5, 21, 34}

def test_Edge_set():
    """
    """
    e = core.Edge(id=42, v_ids=[5, 1])
    e.set_length(93.45)
    assert e.len == pytest.approx(93.45)

    e.set_junction_type('E')
    assert e.junction_type == 'E'
    e.set_junction_type('J1')
    assert e.junction_type == 'J1'

def test_Edge_set_special():
    """
    """
    e = core.Edge(id=42, v_ids=[5, 1])
    assert not e.is_external
    assert not e.is_special
    assert e.theta is None
    e.set_external()
    assert e.is_external
    assert not e.is_special
    assert e.theta == pytest.approx(-1)
    with pytest.raises(ValueError, match="External doesn't have theta"):
        e.set_theta(10)
    assert e.is_external
    e.set_external(False)
    assert not e.is_external
    assert not e.is_special
    assert e.theta is None
    e.set_special()
    assert not e.is_external
    assert e.is_special    
    assert e.theta is None
    e.set_special(False)
    assert not e.is_external
    assert not e.is_special
    assert e.theta is None

    e.set_theta(60)
    assert not e.is_external
    assert not e.is_special
    assert e.theta == pytest.approx(60)
    e.set_theta(58, 15, 58)
    assert not e.is_external
    assert e.is_special
    assert e.theta == pytest.approx(58)
    e.set_theta(12, 15, 58)
    assert not e.is_external
    assert not e.is_special
    assert e.theta == pytest.approx(12)
    e.set_theta(60, 15, 58)
    assert not e.is_external
    assert not e.is_special
    assert e.theta == pytest.approx(60)    
    e.set_theta(30, 15)
    assert not e.is_external
    assert e.is_special
    assert e.theta == pytest.approx(30)
    e.set_theta(30, 15)
    assert not e.is_external
    assert e.is_special
    assert e.theta == pytest.approx(30)    
    e.set_theta(30, upper_thrd=15)
    assert not e.is_external
    assert not e.is_special
    assert e.theta == pytest.approx(30) 
    e.set_special()
    assert not e.is_external
    assert e.is_special
    e.set_theta(-1, 15, 62)
    assert e.is_external
    assert not e.is_special
    with pytest.raises(ValueError, match="External cannot be set special"):
        e.set_special()
    assert e.is_external
    assert not e.is_special
    assert e.theta == pytest.approx(-1)


def test_Edge_from_tess_file():
    """
    """
    filename = 'tests/test_data/n8-id1.tess'
    _edges = core.Edge.from_tess_file(filename)
    assert len(_edges.keys()) == 78
    assert _edges[1].id == 1
    assert _edges[41].__str__() == 'Edge(id=41)'
    assert set(_edges[10].v_ids) == {4, 2}
    assert set(_edges[20].v_ids) == {20, 21}
    for e in _edges.values():
        assert len(e.v_ids) == 2

    _vertices = core.Vertex.from_tess_file(filename)
    _edges = core.Edge.from_tess_file(filename, _vertices)
    assert len(_vertices.keys()) == 41
    assert len(_edges.keys()) == 78
    assert _edges[1].id == 1
    assert _edges[41].__str__() == 'Edge(id=41)'
    assert set(_edges[10].v_ids) == {4, 2}
    assert set(_edges[20].v_ids) == {20, 21}
    for e in _edges.values():
        assert len(e.v_ids) == 2
    assert set(_vertices[1].neighbor_ids) == {2, 3, 5}
    assert len(_vertices[1].neighbor_ids) == 3
    assert set(_vertices[1].e_ids) == {1, 2, 6}
    assert len(_vertices[1].e_ids) == 3
    assert set(_edges[29].neighbor_ids) == {33, 45, 58, 27, 28, 31}
    assert len(_edges[29].neighbor_ids) == 6
    assert set(_edges[59].neighbor_ids) == {2, 3, 10, 60, 61}
    assert len(_edges[59].neighbor_ids) == 5    

    filename = 'tests/test_data/complex.tess'
    _edges = core.Edge.from_tess_file(filename, measure=True)
    assert len(_edges.keys()) == 64
    assert _edges[1].id == 1
    assert _edges[41].__str__() == 'Edge(id=41)'
    assert set(_edges[10].v_ids) == {12, 10}
    assert set(_edges[20].v_ids) == {15, 14}
    for e in _edges.values():
        assert len(e.v_ids) == 2
    assert _edges[1].len == pytest.approx(0.856403573756)
    assert _edges[64].len == pytest.approx(0.305660878901)
    assert _edges[41].len == pytest.approx(0.131174647632)

    filename = 'tests/test_data/n8-id1-2D-reg.tess'
    _edges = core.Edge.from_tess_file(
        filename, measure=True, theta=True, lower_thrd=15)
    assert len(_edges.keys()) == 24
    assert _edges[1].id == 1
    assert _edges[11].__str__() == 'Edge(id=11)'
    assert set(_edges[10].v_ids) == {10, 11}
    assert set(_edges[20].v_ids) == {16, 3}
    for e in _edges.values():
        assert len(e.v_ids) == 2
    assert _edges[1].len == pytest.approx(0.372175178843)
    assert _edges[1].theta == pytest.approx(-1)
    assert _edges[1].is_external
    assert _edges[24].len == pytest.approx(0.282179199432)
    assert _edges[24].theta == pytest.approx(-1)
    assert _edges[24].is_external
    assert not _edges[24].is_special
    assert _edges[4].len == pytest.approx(0.166904842609)
    assert _edges[4].theta == pytest.approx(67.795707673672)
    assert not _edges[4].is_external
    assert _edges[4].is_special
    assert len([e.id for e in _edges.values() if e.is_external]) == 10

    _edges = core.Edge.from_tess_file(
        filename, measure=True, theta=True, lower_thrd=70, upper_thrd=100)
    assert _edges[4].theta == pytest.approx(67.795707673672)
    assert not _edges[4].is_external
    assert not _edges[4].is_special
    assert _edges[5].theta == pytest.approx(99.343932545403)
    assert not _edges[5].is_external
    assert _edges[5].is_special
    assert _edges[5].len == pytest.approx(0.217043601663)
    assert _edges[7].theta == pytest.approx(135.438499725622)
    assert not _edges[7].is_external
    assert not _edges[7].is_special


def test_Face():
    """
    """
    f = core.Face(id=42, v_ids=[5, 1, 2, 7, 8])
    assert f.id == 42
    assert len(f.v_ids) == 5
    assert f.v_ids == [5, 1, 2, 7, 8]
    assert f.__str__() == "Face(id=42)"
    assert f.e_ids == []
    assert f.neighbor_ids == []
    assert f.p_ids == []
    assert not f.is_special
    assert not f.is_external
    assert f.theta is None

def test_Face_add_neighbors():
    """
    """
    f = core.Face(id=42, v_ids=[5, 1, 2, 7, 8])
    f.add_neighbor(21)
    f.add_neighbor(34)
    f.add_neighbors([1, 2])
    f.add_neighbors([5, 1, 3])
    f.add_neighbor(2)
    assert len(f.neighbor_ids) == 6
    assert set(f.neighbor_ids) == {1, 2, 3, 5, 21, 34}


def test_Face_add_incident():
    """
    """
    f = core.Face(id=42, v_ids=[5, 1, 2, 7, 8])
    f.add_incident_poly(21)
    f.add_incident_poly(34)
    f.add_incident_polys([1, 2])
    f.add_incident_polys([5, 1, 3])
    f.add_incident_poly(5)
    assert len(f.p_ids) == 6
    assert f.get_degree() == 6
    assert len(f.incident_cells) == 6
    assert set(f.p_ids) == {1, 2, 3, 5, 21, 34}
    assert set(f.incident_cells) == {1, 2, 3, 5, 21, 34}
    f.add_edges([1, 2, 3, 4, 5])
    f.add_edges([4, 7])
    assert len(f.e_ids) == 6
    assert set(f.e_ids) == {1, 2, 3, 4, 5, 7}


def test_Face_add_equation():
    """
    """
    f = core.Face(id=42, v_ids=[5, 1, 2, 7, 8])
    f.add_equation(
        d=-0.799252301482,
        a=0.012037703346,
        b=-0.758463682782,
        c=-0.651604124909)
    assert f.d == pytest.approx(-0.799252301482)
    assert f.a == pytest.approx(0.012037703346)
    assert f.b == pytest.approx(-0.758463682782)
    assert f.c == pytest.approx(-0.651604124909)
    assert f.normal == pytest.approx(
        (0.012037703346, -0.758463682782, -0.651604124909)
    )


def test_Face_set():
    """
    """
    f = core.Face(id=42, v_ids=[5, 1, 2, 7, 8])
    f.set_seed((0.016887594857, 0.181381736214))
    assert f.seed == pytest.approx((0.016887594857, 0.181381736214))

    f.set_area(0.353327084839)
    assert f.area == pytest.approx(0.353327084839)


def test_Face_set_special():
    """
    """
    f = core.Face(id=42, v_ids=[5, 1, 2, 7, 8])
    assert not f.is_external
    assert not f.is_special
    assert f.theta is None
    f.set_external()
    assert f.is_external
    assert not f.is_special
    assert f.theta == pytest.approx(-1)
    with pytest.raises(ValueError, match="External doesn't have theta"):
        f.set_theta(10)
    assert f.is_external
    f.set_external(False)
    assert not f.is_external
    assert not f.is_special
    assert f.theta is None
    f.set_special()
    assert not f.is_external
    assert f.is_special    
    assert f.theta is None
    f.set_special(False)
    assert not f.is_external
    assert not f.is_special
    assert f.theta is None

    f.set_theta(60)
    assert not f.is_external
    assert not f.is_special
    assert f.theta == pytest.approx(60)
    f.set_theta(58, 15, 58)
    assert not f.is_external
    assert f.is_special
    assert f.theta == pytest.approx(58)
    f.set_theta(12, 15, 58)
    assert not f.is_external
    assert not f.is_special
    assert f.theta == pytest.approx(12)
    f.set_theta(60, 15, 58)
    assert not f.is_external
    assert not f.is_special
    assert f.theta == pytest.approx(60)    
    f.set_theta(30, 15)
    assert not f.is_external
    assert f.is_special
    assert f.theta == pytest.approx(30)
    f.set_theta(30, 15)
    assert not f.is_external
    assert f.is_special
    assert f.theta == pytest.approx(30)    
    f.set_theta(30, upper_thrd=15)
    assert not f.is_external
    assert not f.is_special
    assert f.theta == pytest.approx(30) 
    f.set_special()
    assert not f.is_external
    assert f.is_special
    f.set_theta(-1, 15, 62)
    assert f.is_external
    assert not f.is_special
    with pytest.raises(ValueError, match="External cannot be set special"):
        f.set_special()
    assert f.is_external
    assert not f.is_special
    assert f.theta == pytest.approx(-1)


def test_Face_from_tess_file():
    """
    """
    filename = 'tests/test_data/n8-id1.tess'
    _faces = core.Face.from_tess_file(filename)
    assert len(_faces.keys()) == 46
    assert _faces[1].id == 1
    assert _faces[41].__str__() == 'Face(id=41)'
    assert set(_faces[10].v_ids) == {11, 14, 15}
    assert set(_faces[10].e_ids) == {17, 26, 23}
    assert _faces[10].normal == pytest.approx(
        (-0.0, -0.0, -1.0)
    )
    assert _faces[10].d == pytest.approx(-0.0)
    assert set(_faces[20].v_ids) == {24, 16, 18, 25}
    assert set(_faces[20].e_ids) == {39, 30, 47, 35}
    assert _faces[20].normal == pytest.approx(
        (-0.073582558800, -0.625425063122, -0.776806988550)
    )
    assert _faces[20].d == pytest.approx(-0.692319498228)

    _edges = core.Edge.from_tess_file(filename)
    _faces = core.Face.from_tess_file(filename, _edges)
    assert len(_edges.keys()) == 78
    assert len(_faces.keys()) == 46
    assert _faces[1].id == 1
    assert _faces[41].__str__() == 'Face(id=41)'
    assert set(_faces[10].v_ids) == {11, 14, 15}
    assert set(_faces[10].e_ids) == {17, 26, 23}
    assert _faces[10].normal == pytest.approx(
        (-0.0, -0.0, -1.0)
    )
    assert _faces[10].d == pytest.approx(-0.0)
    
    # assert set(_edges[1].neighbor_ids) == {2, 3, 5}
    # assert len(_edges[1].neighbor_ids) == 3
    # assert set(_edges[1].e_ids) == {1, 2, 6}
    # assert len(_edges[1].e_ids) == 3

    # filename = 'tests/test_data/complex.tess'
    # _edges = core.Edge.from_tess_file(filename, measure=True)
    # assert len(_edges.keys()) == 64
    # assert _edges[1].id == 1
    # assert _edges[41].__str__() == 'Edge(id=41)'
    # assert set(_edges[10].v_ids) == {12, 10}
    # assert set(_edges[20].v_ids) == {15, 14}
    # for e in _edges.values():
    #     assert len(e.v_ids) == 2
    # assert _edges[1].len == pytest.approx(0.856403573756)
    # assert _edges[64].len == pytest.approx(0.305660878901)
    # assert _edges[41].len == pytest.approx(0.131174647632)

    # filename = 'tests/test_data/n8-id1-2D-reg.tess'
    # _edges = core.Edge.from_tess_file(
    #     filename, measure=True, theta=True, lower_thrd=15)
    # assert len(_edges.keys()) == 24
    # assert _edges[1].id == 1
    # assert _edges[11].__str__() == 'Edge(id=11)'
    # assert set(_edges[10].v_ids) == {10, 11}
    # assert set(_edges[20].v_ids) == {16, 3}
    # for e in _edges.values():
    #     assert len(e.v_ids) == 2
    # assert _edges[1].len == pytest.approx(0.372175178843)
    # assert _edges[1].theta == pytest.approx(-1)
    # assert _edges[1].is_external
    # assert _edges[24].len == pytest.approx(0.282179199432)
    # assert _edges[24].theta == pytest.approx(-1)
    # assert _edges[24].is_external
    # assert not _edges[24].is_special
    # assert _edges[4].len == pytest.approx(0.166904842609)
    # assert _edges[4].theta == pytest.approx(67.795707673672)
    # assert not _edges[4].is_external
    # assert _edges[4].is_special
    # assert len([e.id for e in _edges.values() if e.is_external]) == 10

    # _edges = core.Edge.from_tess_file(
    #     filename, measure=True, theta=True, lower_thrd=70, upper_thrd=100)
    # assert _edges[4].theta == pytest.approx(67.795707673672)
    # assert not _edges[4].is_external
    # assert not _edges[4].is_special
    # assert _edges[5].theta == pytest.approx(99.343932545403)
    # assert not _edges[5].is_external
    # assert _edges[5].is_special
    # assert _edges[5].len == pytest.approx(0.217043601663)
    # assert _edges[7].theta == pytest.approx(135.438499725622)
    # assert not _edges[7].is_external
    # assert not _edges[7].is_special


def test_CellComplex():
    """
    """
    filename = 'tests/test_data/n8-id1.tess'
    c = core.CellComplex(filename)

    assert c.source_file == filename, "Filename doesn't match"