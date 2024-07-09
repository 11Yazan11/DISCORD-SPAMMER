import aiohttp
import asyncio
import random
import time
import pygame
import sys
from io import StringIO




class Setup:
    def __init__(self, webhook_url) -> None:
        self.chars = 'abcdefghijklmnopqrstuvwxyz134567890%ù²(-à)*'
        self.webhook_url = webhook_url
        self.usernames = []
        self.contents = []
        self.avatar_urls = []
        self.generate_usernames_list()
        self.generate_contents_list()
        self.generate_avatar_urls_list()

    def generate_usernames_list(self):
        for _ in range(100):
            username = ''.join(random.choice(self.chars) for _ in range(15))
            username = 'D I S C O R D     K I L L E R    ||     VERSION ID  = [' + str(username) + ']'
            self.usernames.append(username)

    def generate_contents_list(self):
        for i in range(100):
            content = "LOADING VIRUS DATA FROM RANDOM USER..." + " " + str(i * (123 / 340)) + " % LOADED"  # random factor
            self.contents.append(content)

    def generate_avatar_urls_list(self):
        any_avatar_url = "https://www.radiofrance.fr/s3/cruiser-production/2020/03/7495829e-7534-4ada-8632-7ee75844e531/870x489_gettyimages-513088279.jpg"
        self.avatar_urls.append(any_avatar_url)
        any_avatar_url = "https://media.teachprivacy.com/wp-content/uploads/2023/07/28143141/Hacker-Funny-AdobeStock_574954979-scaled.jpeg"
        self.avatar_urls.append(any_avatar_url)
        any_avatar_url = "https://as1.ftcdn.net/v2/jpg/05/80/66/52/1000_F_580665262_SbO69iupamlna60JTP3QEUn2I1S9Myi3.jpg"
        self.avatar_urls.append(any_avatar_url)
        any_avatar_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOSbhqsghVrKH5620pPh1wvOw7Fngy4TXi-w&s"
        self.avatar_urls.append(any_avatar_url)
        any_avatar_url = "https://t3.ftcdn.net/jpg/05/74/95/50/360_F_574955028_Y2qisbczKSUUAMkvC4eAIomVPWga22Ix.jpg"
        self.avatar_urls.append(any_avatar_url)
        any_avatar_url = "https://nerdshizzle.com/wp-content/uploads/2021/01/im-a-hacker.jpg"
        self.avatar_urls.append(any_avatar_url)

    def create_random_payload(self, custom_state=False, custom_content=""):
        payload = {
            "username": self.usernames[random.randint(0, len(self.usernames) - 1)],
            "content": self.contents[random.randint(0, len(self.contents) - 1)],
            "avatar_url": self.avatar_urls[random.randint(0, len(self.avatar_urls) - 1)]
        } if not custom_state else {
            "username": self.usernames[random.randint(0, len(self.usernames) - 1)],
            "content": custom_content,
            "avatar_url": self.avatar_urls[random.randint(0, len(self.avatar_urls) - 1)]
        }
        return payload, self.webhook_url


class Sender:
    def __init__(self, webhook_url, payload):
        self.webhook_url = webhook_url
        self.payload = payload

    async def send_webhook_message(self):
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.post(self.webhook_url, json=self.payload) as response:
                    if response.status == 204:
                        print(f"MESSAGE = [{self.payload['content']}]")
                        print(f"USERNAME = [{self.payload['username']}]")
                        print(f"AVATAR_URL = [{self.payload['avatar_url'][0:70]}]")
                        print('SENT SUCCESSFULLY')
                        return
                    elif response.status == 429:  # Rate limited
                        data = await response.json()
                        retry_after = data.get("retry_after", 0.5)
                        print(f"Rate limited. Retrying after {retry_after} seconds.")
                        await asyncio.sleep(retry_after)
                    else:
                        print(f"Failed to send message. Status code: {response.status}")
                        print(await response.text())
                        return



class Displayer:
    def __init__(self):
        pygame.init()
        self.wnx = 600
        self.wny = 600
        self.screen = pygame.display.set_mode((self.wnx, self.wny))
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.spam_font = pygame.font.Font('freesansbold.ttf', 17)
        self.small_font = pygame.font.Font('freesansbold.ttf', 12)
        self.text_input = TextInput(self.spam_font, self.screen)
        self.initialize_texts()
        self.initialize_buttons()
        self.console_output = []
        self.scroll_offset = 0
        self.change_num = False
        self.scroll_cons = False
        self.enabled_send_options_color = (140, 140, 0)
        self.disabled_send_options_color = (95, 95, 0)
        self.custom_state = False


    def initialize_texts(self):
        self.notice_text2 = self.font.render('CLICK HERE TO START SPAMMING...', True, (10, 10, 10))
        self.spam_text = self.spam_font.render('SPAM', True, (20, 65, 65))
        self.console_text = self.font.render('[CONSOLE OUTPUT]', True, (120, 150, 65))
        self.notice_con_text = self.small_font.render('PRESS [C] TO ENABLE CONSOLE SCROLLING, THEN USE [LEFT]/[RIGHT] TO SCROLL, [F] TO CLEAR. ', True, (120, 120, 120), (20, 20, 20))
        self.notice_input_box_text = self.font.render('SEND A CUSTOM MESSAGE...', True, (0, 120, 50))
        self.custom_w = self.spam_font.render('CUSTOM', True, (12, 12, 12))
        self.original_text = self.spam_font.render('ORIGINAL', True, (12, 12, 12))

    def initialize_buttons(self):
        self.spam_button_rect = pygame.Rect(self.wnx / 2 - 30, self.wny/2 + 55, 60, 30)
        self.custom_send_butt = pygame.Rect(140, self.wny/2 - 100, 100, 30)
        self.original_send_butt = pygame.Rect(280, self.wny/2 - 100, 100, 30)

    def draw_static_elements(self, mess_num):
        self.screen.fill((100, 43, 43))
        pygame.display.set_caption("DISCORD SPAMMER CONTROL INTERFACE")
        self.screen.blit(self.notice_text2, (self.wnx / 3 - 60, self.wny / 2 + 25))
        pygame.draw.rect(self.screen, (120, 90, 90), self.spam_button_rect, border_radius=4)
        self.screen.blit(self.spam_text, (self.wnx / 2 - 25, self.wny / 2 + 60))
        pygame.draw.rect(self.screen, (20, 20, 20), (0, self.wny-165, self.wnx, 165))
        self.screen.blit(self.console_text, (self.wnx / 2 - 100, self.wny - 150))
        self.screen.blit(self.notice_con_text, (5, self.wny - 175))

        messnum_text = self.font.render(f'NUMBER OF MESSAGES TO SEND = [{mess_num}]', True, (10, 10, 65))
        messnum_notice_text = self.font.render(f'PRESS [N], THEN USE [UP]/[DOWN] TO MODIFY...', True, (10, 10, 65))
        self.screen.blit(messnum_text, (10, 20))
        self.screen.blit(messnum_notice_text, (10, 50))
        self.screen.blit(self.notice_input_box_text, (self.wnx / 2 - 145, 110))
        if self.custom_state:
            color1 = self.enabled_send_options_color
            color2 = self.disabled_send_options_color
        else:
            color1 = self.disabled_send_options_color
            color2 = self.enabled_send_options_color

        pygame.draw.rect(self.screen, color1, self.custom_send_butt)
        pygame.draw.rect(self.screen, color2, self.original_send_butt)
        self.screen.blit(self.custom_w, (146, self.wny/2 - 95))
        self.screen.blit(self.original_text, (286, self.wny/2 - 95))

    def handle_input(self, mess_num):
        start = False
        pressed = pygame.key.get_pressed()
        self.mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)

        if (self.mouse_rect.colliderect(self.spam_button_rect) and pygame.mouse.get_pressed()[0]):
            start = True
            self.spam_button_rect.x += 2
            self.spam_button_rect.y += 2
        else:
            self.spam_button_rect = pygame.Rect(self.wnx / 2 - 30, self.wny/2 + 55, 60, 30)

        if (self.mouse_rect.colliderect(self.custom_send_butt) and pygame.mouse.get_pressed()[0]):
            self.custom_state = True  
        if (self.mouse_rect.colliderect(self.original_send_butt) and pygame.mouse.get_pressed()[0]):
            self.custom_state = False         

        if pressed[pygame.K_n] and not self.active_text_box:
            time.sleep(0.1)
            self.change_num = not self.change_num

        if pressed[pygame.K_c] and not self.active_text_box:
            time.sleep(0.1)
            self.scroll_cons = not self.scroll_cons

        if pressed[pygame.K_f] and not self.active_text_box:
            time.sleep(0.1)
            self.console_output = []
               

        if self.change_num:
            mess_num = self.change_message_count(mess_num, pressed)

        if self.scroll_cons:
            self.handle_console_scrolling(pressed)

        return start, mess_num

    def change_message_count(self, mess_num, pressed):
        if pressed[pygame.K_UP] and mess_num < 50 and not self.active_text_box:  # avoid timeout from Discord
            mess_num += 1
            time.sleep(0.1)
        if pressed[pygame.K_DOWN] and mess_num > 0 and not self.active_text_box:
            mess_num -= 1
            time.sleep(0.1)
        return mess_num

    def handle_console_scrolling(self, pressed):
        if pressed[pygame.K_LEFT] and not self.active_text_box:
            self.scroll_offset = min(self.scroll_offset + 1, len(self.console_output) - 1)
            time.sleep(0.1)
        if pressed[pygame.K_RIGHT] and not self.active_text_box:
            self.scroll_offset = max(self.scroll_offset - 1, 0)
            time.sleep(0.1)

    def display_console_output(self):
        for i, line in enumerate(self.console_output[-8-self.scroll_offset:-self.scroll_offset] if self.scroll_offset else self.console_output[-8:]):
            console_line_text = self.small_font.render(line, True, (20, 200, 20))
            self.screen.blit(console_line_text, (10, self.wny - 115 + i * 10))

    def updater(self, mess_num, active_text_box):
        self.custom_text = self.text_input.return_final_text_only()
        self.active_text_box = active_text_box
        self.draw_static_elements(mess_num)
        start, mess_num = self.handle_input(mess_num)
        self.display_console_output()
        self.text_input.draw()  # Draw the input box
        pygame.display.flip()
        return start, mess_num
    
    def handle_event(self, event):
        a = self.text_input.handle_event(event, self.custom_state)
        return a 

    def add_console_output(self, text):
        self.console_output.append(text)
        if len(self.console_output) > 100:
            self.console_output.pop(0)

       
            




class ConsoleCapture:
    def __init__(self, displayer):
        self.displayer = displayer
        self.buffer = StringIO()

    def write(self, text):
        self.buffer.write(text)
        self.displayer.add_console_output(text.strip())

    def flush(self):
        pass


class TextInput:
    def __init__(self, font, screen) -> None:
        self.font = font
        self.screen = screen
        self.input_box = pygame.Rect(160, 150, 140, 32)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.to_send = False
        self.final_text = ''

    def handle_event(self, event, custom_state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN and custom_state == True:
                    self.to_send = True
                    self.final_text = self.text
                    self.text = ''
                    self.active = False
                    self.color = self.color_active if self.active else self.color_inactive

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key != pygame.K_RETURN:
                    self.text += event.unicode
        return self.active            

    def draw(self):
        txt_surface = self.font.render(self.text, True, self.color)
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)

    def get_data(self):
        if self.to_send:
            self.to_send = False
            return True, self.final_text
        return False, ''   
    def return_final_text_only(self):
        return self.final_text




async def main():
    webhook_link = input("ENTER WEBHOOK LINK PLEASE...( Only enter the link, nothing else. ) || ")
    displayer = Displayer()
    keep_data = False
    number_of_messages = 3
    setup = Setup(webhook_link)
    tasks = []

    # Redirect stdout to capture print statements
    original_stdout = sys.stdout
    sys.stdout = ConsoleCapture(displayer)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            writing = displayer.handle_event(event)  # Handle events for the input box

        start, number_of_messages = displayer.updater(number_of_messages, writing)

        to_send, txt_to_send = displayer.text_input.get_data()  # Check for input box data
        
        if to_send:
            tasks = []
            payload, webhook = setup.create_random_payload(to_send, txt_to_send)
            sender = Sender(webhook, payload)
            tasks.append(sender.send_webhook_message())
            await asyncio.gather(*tasks)


        elif start:
            tasks = []
            if not keep_data:
                for _ in range(number_of_messages):
                    payload, webhook = setup.create_random_payload()
                    sender = Sender(webhook, payload)
                    tasks.append(sender.send_webhook_message())
            else:
                payload, webhook = setup.create_random_payload()
                sender = Sender(webhook, payload)
                for _ in range(number_of_messages):
                    tasks.append(sender.send_webhook_message())

            await asyncio.gather(*tasks)

    # Restore original stdout
    sys.stdout = original_stdout

if __name__ == "__main__":
    asyncio.run(main())

