# install.packages("ggplot2")
library(ggplot2)

set.seed(10)
df.rnorm <- data.frame(rnorm = rnorm(1000000, mean = 60000, sd = 10000))

ggplot(data = df.rnorm, aes(x = rnorm)) +
  geom_histogram(bins = 500) +
  geom_vline(xintercept = 40000, color = "red", linetype = "dashed") +
  annotate("text", label = "Potential ", x = 40000, y = 1250, color = "white")+
  geom_vline(xintercept = 60000, color = "orange", linetype = "dashed") +
  annotate("text", label = "Average", x = 60000, y = 5000, color = "white")+
  geom_vline(xintercept = 80000, color = "green", linetype = "dashed") +
  annotate("text", label = "Exceptional", x = 0000, y = 7500, color = "white") +
  theme_dark()
