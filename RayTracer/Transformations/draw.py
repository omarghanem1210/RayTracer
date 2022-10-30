from RayTracer.Transformations.transformations import *
from RayTracer.Features.background import *

ray_origin = Vector(0, 0, -5)
wall_z = 10
wall_size = 7
half = wall_size / 2

canvas = Canvas(200, 200)
color = Color(1, 0, 0)
m = Material(color=Color(1, 0.2, 1))
shape = Sphere(sphere_material=m)

light_position = Vector(-10, 10, -10)
light_color = Color(1, 1, 1)
light = Light(light_position, light_color)
pixel_size = wall_size / 200


for y in range(200):
    world_y = half - pixel_size * y
    for x in range(200):
        world_x = -half + pixel_size * x
        position = Vector(world_x, world_y, wall_z)
        r = Ray(ray_origin, (position - ray_origin).normalize())
        xs = r.intersect(shape)
        h = hit(xs)

        if h.t is not None:
            point = r.position(h.t)
            normal = h.obj.normal_at(point)
            eye = -((position - ray_origin).normalize())
            color = lighting(h.obj.sphere_material, light, point, eye, normal)
            canvas.write_pixel(x, y, color)
canvas.to_png('D:/Programming/Ray_Tracer/Images/circle.png')



