import argparse
import sys
import signal
from os import path

from uldlib import downloader, captcha,  __version__, __path__, result

def run():
    parser = argparse.ArgumentParser(
        description='Download file from Uloz.to using multiple parallel downloads.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('url', metavar='URL', type=str,
                        help="URL from Uloz.to (tip: enter in 'quotes' because the URL contains ! sign)")
    parser.add_argument('--parts', metavar='N', type=int, default=10,
                        help='Number of parts that will be downloaded in parallel')
    parser.add_argument('--output', metavar='DIRECTORY', type=str, default="./", 
                        help='Target directory')
    parser.add_argument('--auto-captcha', default=False, action="store_true",
                        help='Try to solve captchas automatically using TensorFlow')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--notify-url', metavar='URL', type=str, default="",
                        help='Notify URL')

    args = parser.parse_args()
    if args.auto_captcha:
        model_path = path.join(__path__[0], "model.tflite")
        model_download_url = "https://github.com/JanPalasek/ulozto-captcha-breaker/releases/download/v2.2/model.tflite"
        captcha_solve_fnc = captcha.AutoReadCaptcha(
            model_path, model_download_url)
    else:
        captcha_solve_fnc = captcha.tkinter_user_prompt

    d = downloader.Downloader(captcha_solve_fnc)
    r = result.Result(args.notify_url)

    # Register sigint handler
    def sigint_handler(sig, frame):
        d.terminate()
        r.log('Program terminated.')
        sys.exit(1)

    signal.signal(signal.SIGINT, sigint_handler)

    d.download(args.url, r, args.parts, args.output)
    d.terminate()