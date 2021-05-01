  setwd("C:/Users/TheCO/OneDrive/Escritorio") # Ruta de trabajo establecida

data = read.csv(file = "Dataset editado 2.csv") # Se sube el modelo de datos inicial

library(dplyr) # Librería de manipulación de datos

str(data) # Revisión inicial de lo
# Asignar formato fecha a las variables correspondientes
data$Fecha.Analisis = as.Date(data$Fecha.Analisis, format = "%d-%m-%Y")
data$FechaExpedido = as.Date(data$FechaExpedido, format = "%d-%m-%Y")
data$FechaVecimiento = as.Date(data$FechaVecimiento, format = "%d-%m-%Y")


# Se crean dos filtros y se crea una columna. Se crea filtro para quitar montos de cero
# Se crea variable de plazo original y se crea filtro para no coger pagos de contado
data = data %>%
  filter(Monto != 0) %>%
  mutate(plazo = FechaVecimiento - FechaExpedido) %>%
  filter(plazo != 0)
  
# Para eliminar NAs de moneda en Ecuador, se remplazan por dólares
index = which(data$Pais == "Ecuador" & data$Moneda == "#N/A")

data[index, 7] = "USD"


# Eliminamos outliers de monto teniendo en cuenta solo lo que está de cuartil 95 para abajo
qnt = quantile(data$Monto, probs = c(0.01, 0.95), na.rm = T)[2]
data2 = data[which(data$Monto < qnt),]

hist(data2$Monto[data$Moneda == "USD"])
hist(data2$Monto[data$Moneda == "Local"])


# Para eliminar el resto de NAs en moneda, se parte de la premisa de menor distancia entre
# monto de la observación y la mediana por país y moneda
# Empezamos entonces hallando estas medianas

pp_median = data2 %>%
  group_by(Pais) %>%
  summarise(local_average = median(Monto[Moneda == "Local"]),
            usd_average = median(Monto[Moneda == "USD"]))

pp_mean = data2 %>%
  group_by(Pais) %>%
  summarise(local_average = mean(Monto[Moneda == "Local"]),
            usd_average = mean(Monto[Moneda == "USD"]))


final_data_set = merge(data2, pp_median, by.x = "Pais", by.y = "Pais")
index = which(final_data_set$Moneda == "#N/A" & final_data_set$Pais == "Peru" & 
        abs(final_data_set$Monto - final_data_set$local_average)
      < abs(final_data_set$Monto - final_data_set$usd_average))

# Ya luego se empiezan a hacer los remplazos pertinentes

final_data_set[index, 7] = "Local"

index = which(final_data_set$Moneda == "#N/A" & final_data_set$Pais == "Peru" & 
                abs(final_data_set$Monto - final_data_set$local_average)
              > abs(final_data_set$Monto - final_data_set$usd_average))

final_data_set[index, 7] = "USD"



index = which(final_data_set$Moneda == "#N/A" & final_data_set$Pais == "Colombia" & 
                abs(final_data_set$Monto - final_data_set$local_average)
              < abs(final_data_set$Monto - final_data_set$usd_average))

final_data_set[index, 7] = "Local"

index = which(final_data_set$Moneda == "#N/A" & final_data_set$Pais == "Colombia" & 
                abs(final_data_set$Monto - final_data_set$local_average)
              > abs(final_data_set$Monto - final_data_set$usd_average))

final_data_set[index, 7] = "USD"

# Comprobación de que no quedó ningún NA en moneda

"#N/A" %in% final_data_set$Moneda

# Eliminamos columnas que ya no son necesarias

final_data_set$Terminos.de.pago = NULL
final_data_set$DiaExpedido = NULL
final_data_set$MesExpedido = NULL
final_data_set$YearExpedido = NULL
final_data_set$Acuerdo.de.pago = NULL
final_data_set$DiaVencimiento = NULL
final_data_set$YearVencimiento = NULL
final_data_set$FechaExpedido = NULL
final_data_set$FechaVecimiento = NULL
final_data_set$Fecha.Analisis = NULL
final_data_set$Factura = NULL
final = final_data_set[,-c(9, 10)]

# Revisamos si hay datos vacios en la unidad de negocio

table(final_data_set$Unidad)

# Se establece que vencimiento negativo será igual a uno (mal cliente)

final$VencimientoBinario = 0
index = which(final$Vencimiento < 0)
final$VencimientoBinario[index] = 1

table(final$VencimientoBinario)

final$Vencimiento = NULL

# Para crear probabilidad de default, se usa aproximación frecuentista

prob = table(final$Cliente, final$VencimientoBinario)

clients = rownames(prob)
PD = c()

for (i in 1:dim(prob)[1]){
  sum_tmp = sum(prob[i, 1:2])
  PD = c(PD, round(prob[i, 2]/sum_tmp, 2))
}

clients_default = data.frame(Clients = clients, Prob_D = PD)

#AL final ya queda la probabilidad de default

final_v2 = merge(x = final, y = clients_default, by.x = "Cliente", by.y = "Clients")

# Se presenta una propuesta de provisiones según pérdida esperada 

Provisiones = final_v2 %>%
  mutate(PE = Prob_D * Monto) %>%
  group_by(Pais, Moneda) %>%
  summarise(suma = sum(PE))
  
# Exportamos archivo csv

write.csv(final_v2, file = "data_set.csv")

