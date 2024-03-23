from faker import Faker

fake = Faker()

def generate_insert_sql(num_records):
    with open("data.txt", "w") as file:
        for _ in range(num_records):
            title = fake.unique.catch_phrase()  # Generates unique titles
            author = fake.name() 
            description = fake.paragraph(nb_sentences=3)  # Generates a short book description
            price = fake.random_number(digits=2) / 10.0
            stock = fake.random_number(digits=3)
            sql_statement = f"INSERT INTO Products (name, description, price, stock) VALUES ('{title} by {author}', '{description}', {price}, {stock});\n"
            file.write(sql_statement)

# Generate and print insert SQL statements for 100 book records
generate_insert_sql(100)
