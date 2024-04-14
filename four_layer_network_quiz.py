def four_layer_network_quiz():
  import random
  statements = {
    "Application": [
        "This layer is the topmost layer of the network model, closest to the end-user.",
        "It provides services directly to the user, such as email, file transfer, and web browsing.",
        "Protocols like HTTP, FTP, SMTP, and DNS operate at this layer.",
        "This layer handles data formatting, encoding, and presentation to the user.",
        "It relies on lower layers to establish connections and transport data reliably."
    ],
    "Transport": [
        "This layer ensures reliable delivery of data between the source and destination processes.",
        "It segments data into smaller units called segments and reassembles them at the receiving end.",
        "TCP (Transmission Control Protocol) and UDP (User Datagram Protocol) are examples of protocols at this layer.",
        "This layer provides end-to-end error detection and recovery mechanisms.",
        "It establishes and maintains end-to-end connections between applications."
    ],
    "Network": [
        "This layer is responsible for routing packets between different networks.",
        "It uses IP (Internet Protocol) addresses to identify devices on the network.",
        "Routers operate at this layer to forward packets based on their destination IP addresses.",
        "This layer performs logical addressing and determines the best path for data transmission.",
        "It handles packet fragmentation and reassembly when necessary."
    ],
    "Data Link": [
        "This layer facilitates reliable data transfer between adjacent network nodes.",
        "It detects and corrects errors that may occur in the physical layer.",
        "Ethernet and Wi-Fi are examples of protocols at this layer.",
        "This layer defines the format of data frames and provides flow control.",
        "It uses MAC (Media Access Control) addresses to identify devices within a local network segment."
    ]
}
  
  def play_game():
      score = 0
      total_questions = 10
      valid_layers = ["application", "transport", "network", "data link"]

      print("Welcome to the Four-Layer Network Model Game!")
      print("For each statement, enter the corresponding layer:")
      print("Application, Transport, Network, or Data Link\n")
      print("Type 'quit' to exit the game.\n")

      for _ in range(total_questions):
          layer = random.choice(list(statements.keys()))
          statement = random.choice(statements[layer])

          while True:
              print("")
              user_answer = input(f"Statement: {statement}\nYour answer: ").strip().lower()

              if user_answer == "quit":
                  print(f"Game exited early. Your final score: {score}/{total_questions}")
                  return
              elif user_answer in valid_layers:
                  if user_answer == layer.lower():
                      print("Correct!")
                      score += 1
                      break
                  else:
                      print(f"Incorrect. Try again.")
              else:
                  print("Invalid answer. Please enter one of the four layers: Application, Transport, Network, or Data Link.")

          print()

      print(f"Game over! Your score: {score}/{total_questions}")

  play_game()
