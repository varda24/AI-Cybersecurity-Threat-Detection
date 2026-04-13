import matplotlib.pyplot as plt

def plot_distribution(y):
    plt.figure()
    y.value_counts().plot(kind='bar')

    plt.title("Normal vs Attack Distribution")
    plt.xlabel("Class (0 = Normal, 1 = Attack)")
    plt.ylabel("Count")

    plt.savefig("outputs/class_distribution.png")
    print("✅ Class distribution graph saved!")