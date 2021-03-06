import urllib3
import json

class Chatfuel:
    
    response = []
    attributes = {}

    def __init__(self, debug = False):
        self.response = []
        self.attributes = {}


    def __del__(self,):
        class_name = self.__class__.__name__
        print (class_name, "destroyed")


    def get_response(self):
        if len(self.response) > 0:
            try:
                return json.dumps({
                    # added this
                    'set_attributes': self.attributes,
                    'messages' : self.response
                })
            except:
                raise
        else:
            try:
                return json.dumps({
                    'set_attributes': self.attributes
                })
            except:
                raise

    # added
    def setAttrinutes(self, attributes):
        if not isinstance(attributes, dict):
            raise ValueError("Error: attributes parameter must be of type dict")
        else:
            self.attributes = attributes

    # added
    def redirectToBlocks(self, block_names):
        if not isinstance(block_names, list):
            raise ValueError("Error: block_names must be of type list")
        else:
            return json.dumps({
                "redirect_to_blocks": block_names
            })

    def sendText(self, messages = None):
        if messages is None:
            raise ValueError('Invalid input message is null!')
        if isinstance(messages, str) or isinstance(messages, unicode):
            self.response.append({'text': messages})
        elif isinstance(messages, list):
            for message in messages:
                self.response.append({'text': messages})
        else:
            raise ValueError('Error: "Text" are not List!')


    def sendImage(self, url_image):
        if self._isURL(url_image):
            self.createAttachment('image', {'url': url_image})
        else:
            raise ValueError('Error: Invalid URL!')


    def sendVideo(self, url):
        if self._isURL(url):
            self.createAttachment('video', {'url': url})
        else:
            raise ValueError('Error: Invalid URL!')


    def sendAudio(self, url):
        if self._isURL(url):
            self.createAttachment('audio', {'url': url})
        else:
            raise ValueError('Error: Invalid URL!')


    def sendTextCard(self, text, buttons):
        for item in buttons:
            if item['type'] == 'element_share':
                raise ValueError("Text Card don't support Button Share!")
            self.createAttachment('template', {
                'template_type' : 'button',
                'text'          : text,
                'buttons'       : buttons
            })
            return True
        return False


    def sendGallery(self, elements):
        if isinstance(elements, list):
            self.createAttachment('template', {
                'template_type' : 'generic',
                "image_aspect_ratio": "square",
                'elements'      :  elements
            })
            return True
        return False


    def sendList(self, elements):
        if len(elements) > 4:
            raise ValueError('Maximum 4 items in Elements for List!')
        if len(elements) < 2:
            raise ValueError('Minimum 2 items in Elements for List!')
        if isinstance(elements, list):
            self.createAttachment('template', {
                'template_type' : 'list',
                'top_element_style' : 'large',
                'elements'      :  elements
            })
            return True
        return False


    def sendQuickReply(self, text, quickReplies):
        if isinstance(quickReplies, list):
            self.response.append({
                'text': text,
                'quick_replies': quickReplies
            })
        else:
            raise ValueError('Error: "Quick replies" are not List!')

    def createElement(self, title, image, subTitle, buttons):
        if self._isURL(image) and isinstance(buttons, list):
            return {
                'title'     : title,
                'image_url' : image,
                'subtitle'  : subTitle,
                'buttons'   : buttons
                }
        else:
            raise ValueError('Buttons are not List!')
        return False

    def createReceipt(self, recipient_name, order_number, payment_method, order_url, timestamp, address, summary, adjustments, elements, currency="USD"):
        if not isinstance(address, dict):
            raise ValueError("Error: address parameter must be a dict.")
        elif not isinstance(summary, dict):
            raise ValueError("Error: summary parameters must be a dict.")
        elif not isinstance(adjustments, list):
            raise ValueError("Error: adjustments parameters must be a list of dict.")
        elif not isinstance(elements, list):
            raise ValueError("Error: elements parameters must be a list of dict.")
        else:
            self.createAttachment('template', {
                "template_type": "receipt",
                "recipient_name": recipient_name,
                "order_number": order_number,
                "currency": currency, 
                "payment_method": payment_method,
                "order_url": order_url,
                "timestamp": timestamp,
                "address": address,
                "summary": summary,
                "adjustments": adjustments,
                "elements": elements
            })

    def createButtonToBlock(self, title, block, setAttributes = None):
        button = {}
        button['type'] = 'show_block'
        button['title'] = title
        if isinstance(block, list):
            button['block_names'] = block
        else:
            button['block_name'] = block
        if not isinstance(setAttributes, dict):
            raise ValueError('Attributes are not Dict!')
        if setAttributes and isinstance(setAttributes, dict):
            button['set_attributes'] = setAttributes
        return button


    def createButtonToURL(self, title, url):
        if self._isURL(url):
            button = {}
            button['type'] = 'web_url'
            button['url'] = url
            button['title'] = title
            return button
        return False


    def createPostBackButton(self, title, url_plugin):
        if self._isURL(url_plugin):
            return {
                    'url'   : url_plugin,
                    'type'  : 'json_plugin_url',
                    'title' : title
                }
        return False


    def createCallButton(self, title, phoneNumber):
        return {
                'type'         : 'phone_number',
                'phone_number' : phoneNumber,
                'title'        : title,
            }


    def _createShareButton(self):
        return {
                'type' : 'element_share'
            }


    def createAttachment(self, _type, payload):
        _type = _type.lower()
        list_type = ['image', 'video', 'audio', 'template']
        if _type in list_type:
            self.response.append({
                "attachment": {
                        "type"      : _type,
                        "payload"   : payload
                    }
                })
        else:
            raise ValueError('Error: "Type" are not List!')


    def _isURL(self, url):
        try:
            if not url:
                raise ValueError ('Not found url!')
            http = urllib3.PoolManager()
            r = http.request('GET', url)
            if r.status == 200:
                return 1
            else:
                raise ValueError( url + ' Not url or url die!')
        except:
            raise
