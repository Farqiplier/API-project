import requests, os, webbrowser
from PIL import Image

#Choose an endpoint
search_type = input("Do you want to search on location, episode or character? ").lower()

# Set the file path for the html file
html_file_path = r"C:\Users\TAKR211206\OneDrive - MOSA-RT\2024 - 2025\API project"

#Put the chosen endpoint in the 'url' variable
if search_type in ['location', 'episode', 'character']: 
    if search_type == 'location':
        url = "https://rickandmortyapi.com/api/location"
    elif search_type == 'episode':
        url = "https://rickandmortyapi.com/api/episode"
    else:  # character
        url = "https://rickandmortyapi.com/api/character"

    page = 1
    while True:
        response = requests.get(f"{url}?page={page}")
        data = response.json()
        names = [item['name'] for item in data['results']]
        
        print(f"Page {page}/{data['info']['pages']}:") 
        for index, name in enumerate(names, start=(page - 1) * 20 + 1):  # Calculate how many pages there are in total
            print(f"{index}. {name}")

        print('\nTo navigate pages: \nType "page X" to go to a specific page, "back" to go to the previous page or "next" to go to the next page. \n\nTo search: \nType a number to search by ID, or type the name.\n')
        user_input = input("Your input: ").strip().lower()

        # If input starts with page, go to chosen page
        if user_input.startswith("page "):
            try:
                new_page = int(user_input.split()[1])
                if new_page > 0 and new_page <= data['info']['pages']:
                    page = new_page
                else:
                    print("Invalid page number.")
            except (ValueError, IndexError):
                print("Please enter a valid page number.\n")

        # If input is back, go back one page
        elif user_input == "back":
            if page > 1:
                page -= 1
            else:
                print("You are already on the first page.\n")
        
        # If input is next, go to the next page 
        elif user_input == "next":
            if page < data['info']['pages']:
                    page += 1
            else:
                print("You are already on the last page.\n")


        else:  

            # If input start with a digit, set the searching to id search
            if user_input.isdigit(): # Check if the input is a number
                # Search the api with the id
                url_id = f"{url}/{user_input}"
                response_id = requests.get(url_id)
                endpoint = response_id.json() # sets the endpoint's search on id search

            # Else set searching to name search
            else:
                try:
                    url_name = f"{url}?name={user_input}"
                    response_name = requests.get(url_name)
                    data_name = response_name.json() 
                    if data_name['results']:  # Check if the response contains a name to set the search mode
                        endpoint = data_name['results'][0] # sets the endpoint's search on name search
                except: 
                    print("No results for this item.")
                    break

            # Check if the item inputted is in the selected endpoint
            if 'name' in endpoint:  
                print(f"Name: {endpoint['name']}")

                # Print info based on which endpoint is selected
                if search_type == 'location':
                    print(f"Type: {endpoint['type']}")
                    print(f"Dimension: {endpoint['dimension']}")
                    
                    # Get all residents of a certain location
                    resident_names = []
                    for resident_url in endpoint['residents']:
                        response = requests.get(resident_url)
                        resident_data = response.json()
                        resident_names.append(resident_data['name'])
                    print(f"Residents: {', '.join(resident_names)}") 

                elif search_type == 'episode':
                    print(f"Air Date: {endpoint['air_date']}")
                    print(f"Episode: {endpoint['episode']}")

                    character_names = []
                    for character_url in endpoint['characters']:
                        response = requests.get(character_url)
                        character_data = response.json()
                        character_names.append(character_data['name'])
                    print(f"Characters: {', '.join(character_names)}") 

                elif search_type == 'character':
                    with Image.open(requests.get(endpoint['image'], stream=True).raw) as img:
                        img.show() 
                    print(f"Status: {endpoint['status']}")
                    print(f"Species: {endpoint['species']}")
                    print(f"Type: {endpoint['type']}")
                    print(f"Gender: {endpoint['gender']}")
                    print(f"Origin: {endpoint['origin']['name']}")
                    print(f"Location: {endpoint['location']['name']}")
                    
                    # Extract and print only episode numbers
                    episode_numbers = [episode_url.split('/')[-1] for episode_url in endpoint['episode']]
                    print(f"Episodes: {', '.join(episode_numbers)}") 

                    print(f"URL: {endpoint['url']}")
                    print(f"Created: {endpoint['created']}")

                # Ask if the user wants to open item with info in the browser
                open_browser = input("Do you want to open this in your browser? (yes/no) ").lower()
                if open_browser == 'yes':
                    if search_type == 'location':
                        resident_images = []
                        for resident_url in endpoint['residents']:
                            response = requests.get(resident_url)
                            resident_data = response.json()
                            resident_images.append({
                                'name': resident_data['name'],
                                'image': resident_data['image']
                            })

                        # Generate HTML for resident images
                        resident_images_html = ""
                        for resident in resident_images:
                            resident_images_html += f"""
                            <div class="image-container"> 
                                <img src="{resident['image']}" alt="{resident['name']}" class="resident-image small-image"> 
                            </div>
                            """
                        
                        # The html content for the location
                        html_content = f"""
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>{endpoint['name']}</title>
                            <link rel="stylesheet" href="Styles.css"> 
                        </head>
                        <body>
                            <div class="text-block"> 
                                <h1>{endpoint['name']}</h1>
                                <p><strong>Type:</strong> {endpoint['type']}</p>
                                <p><strong>Dimension:</strong> {endpoint['dimension']}</p>
                                <p><strong>Residents:</strong> {', '.join(resident_names)}</p>
                                <p><strong>URL:</strong> <a href="{endpoint['url']}">{endpoint['url']}</a></p>
                                <p><strong>Created:</strong> {endpoint['created']}</p>
                            </div>
                            
                            <div class="button-group">
                                <button onclick="changeImageSize('small')">Small</button>
                                <button onclick="changeImageSize('medium')">Medium</button>
                                <button onclick="changeImageSize('big')">Big</button>
                            </div>

                            <div class="more-images-block">
                                {resident_images_html}
                            </div>
                            
                            <script> 
                                function changeImageSize(size) {{
                                    var images = document.querySelectorAll('.resident-image');
                                    images.forEach(function(image) {{
                                        if (size === 'small') {{
                                            image.style.maxWidth = '100px'; 
                                        }} else if (size === 'medium') {{
                                            image.style.maxWidth = '150px'; 
                                        }} else if (size === 'big') {{
                                            image.style.maxWidth = '200px'; 
                                        }}
                                    }});
                                    const buttons = document.querySelectorAll('.button-group button');
                                    
                                    buttons.forEach(button => {{
                                        // 3. Check if the button's text content matches the selected size.
                                        if (button.textContent.toLowerCase() === size) {{
                                            button.classList.add('selected'); // Add the 'selected' class.
                                        }} else {{
                                            button.classList.remove('selected'); // Remove 'selected' from other buttons.
                                        }}
                                    }}); 
                                }}
                                changeImageSize('small'); // Call the function to set default size on page load
                                
                            </script>
                        </body>
                        </html>
                        """
                    
                    # The html content for the episode
                    elif search_type == 'episode':
                        # Fetch character images (similar to resident images)
                        character_images = []
                        for character_url in endpoint['characters']:
                            response = requests.get(character_url)
                            character_data = response.json()
                            character_images.append({
                                'name': character_data['name'],
                                'image': character_data['image']
                            })

                        # Generate HTML for resident images
                        character_images_html = ""
                        for character in character_images:
                            character_images_html += f"""
                            <div class="image-container"> 
                                <img src="{character['image']}" alt="{character['name']}" class="character-image small-image"> 
                            </div>
                            """

                        html_content = f"""
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>{endpoint['name']}</title>
                            <link rel="stylesheet" href="Styles.css"> 
                        </head>
                        <body>
                            <div class="text-block">
                                <h1>{endpoint['name']}</h1>
                                <p><strong>Air Date:</strong> {endpoint['air_date']}</p>
                                <p><strong>Episode:</strong> {endpoint['episode']}</p>
                                <p><strong>characters:</strong> {', '.join(character_names)}</p>
                                <p><strong>URL:</strong> <a href="{endpoint['url']}">{endpoint['url']}</a></p>
                                <p><strong>Created:</strong> {endpoint['created']}</p>
                            </div>
                            
                            <div class="button-group">
                                <button onclick="changeImageSize('small')">Small</button>
                                <button onclick="changeImageSize('medium')">Medium</button>
                                <button onclick="changeImageSize('big')">Big</button>
                            </div>

                            <div class="more-images-block">
                                {character_images_html}
                            </div>

                            <script> 
                                function changeImageSize(size) {{
                                    var images = document.querySelectorAll('.character-image');
                                    images.forEach(function(image) {{
                                        if (size === 'small') {{
                                            image.style.maxWidth = '100px'; 
                                        }} else if (size === 'medium') {{
                                            image.style.maxWidth = '150px'; 
                                        }} else if (size === 'big') {{
                                            image.style.maxWidth = '200px'; 
                                        }}
                                    }});
                                    const buttons = document.querySelectorAll('.button-group button');

                                    buttons.forEach(button => {{
                                        // 3. Check if the button's text content matches the selected size.
                                        if (button.textContent.toLowerCase() === size) {{
                                            button.classList.add('selected'); // Add the 'selected' class.
                                        }} else {{
                                            button.classList.remove('selected'); // Remove 'selected' from other buttons.
                                        }}
                                    }}); 
                                }}
                                changeImageSize('small'); // Call the function to set default size on page load
                                
                            </script>

                        </body>
                        </html>
                        """

                        # The html content for the character
                    elif search_type == 'character':
                        html_content = f"""
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>{endpoint['name']}</title>
                            <link rel="stylesheet" href="Styles.css"> 
                        </head>
                        <body>
                            <div class="text-block">
                                <h1>{endpoint['name']}</h1>
                                <img src="{endpoint['image']}" alt="{endpoint['name']}">
                                <p><strong>Status:</strong> {endpoint['status']}</p>
                                <p><strong>Species:</strong> {endpoint['species']}</p>
                                <p><strong>Type:</strong> {endpoint['type']}</p>
                                <p><strong>Gender:</strong> {endpoint['gender']}</p>
                                <p><strong>Origin:</strong> {endpoint['origin']['name']}</p>
                                <p><strong>Location:</strong> {endpoint['location']['name']}</p>
                                <p><strong>Episodes:</strong> {', '.join(episode_numbers)}</p>
                                <p><strong>URL:</strong> <a href="{endpoint['url']}">{endpoint['url']}</a></p>
                                <p><strong>Created:</strong> {endpoint['created']}</p>
                            </div>
                        </body>
                        </html>
                        """

                        #
                    html_file_path = os.path.join(html_file_path, f"{endpoint['name'].replace(' ', '_')}.html")
                    with open(html_file_path, 'w') as html_file:
                        html_file.write(html_content)

                    webbrowser.open(f"file://{os.path.abspath(html_file_path)}")
                    print(f"Web page for {endpoint['name']} opened in browser.") 
                    break