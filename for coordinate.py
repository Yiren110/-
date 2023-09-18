%matplotlib inline
import matplotlib.pyplot as plt
# 你的绘图代码
plt.plot([1, 2, 3], [4, 5, 6])
plt.show()
def read_strokes_from_txt(filename="D:/project/for2/strokes.txt"):
    strokes = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            stroke = []
            points = line.strip().split(";")
            for point in points:
                point = point.replace("(", "").replace(")", "")  # 去掉括號
                x, y = map(int, point.split(","))
                stroke.append((x, y))
            strokes.append(stroke)
    return strokes

def plot_strokes(strokes):
    plt.figure(figsize=(10, 10))
    for stroke in strokes:
        x_coords = [x for x, y in stroke]
        y_coords = [y for x, y in stroke]
        plt.plot(x_coords, y_coords)
    plt.gca().invert_yaxis()  # 可能需要這一行，取決於你的座標系統
    plt.show()

if __name__ == "__main__":
    strokes = read_strokes_from_txt()
    plot_strokes(strokes)
