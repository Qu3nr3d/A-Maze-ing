from mlx import Mlx

m = Mlx()
mlx_ptr = m.mlx_init()
if mlx_ptr is None:
    raise RuntimeError("mlx_init() failed")
win_ptr = m.mlx_new_window(mlx_ptr, 640, 480, "kgirczyc")


def on_key(keycode, param):
    if keycode == 65307:  # Escape
        m.mlx_loop_exit(mlx_ptr)


m.mlx_hook(win_ptr, 2, 1, on_key, None)  # event 2 = KeyPress
m.mlx_loop(mlx_ptr)
m.mlx_destroy_window(mlx_ptr, win_ptr)
m.mlx_release(mlx_ptr)
m.mlx_key_hook(win_ptr, on_key, 65307)