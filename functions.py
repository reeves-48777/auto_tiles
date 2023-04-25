## create a function that compute images per second
def compute_fps(render_time):
    # print(f"Render time: {render_time}")
    return round(1 / render_time)

def compute_average_fps(fps_list):
    return round(sum(fps_list) / len(fps_list))