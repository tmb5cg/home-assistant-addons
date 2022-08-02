const puppeteer = require('puppeteer');

(async () => { 

    const browser = await puppeteer.launch({
        'headless':false,
        'slowMo': 50
    });

    //page
    const page = await browser.newPage();

    await page.goto('https://uppy.io/examples/xhrupload/', {'waitUntil': 'networkidle2'});

    const [fileChooser] = await Promise.all([
        page.waitForFileChooser(),
        page.click('.uppy-FileInput-btn')
    ])

    await fileChooser.accept(['/Users/tucker/Documents/GitHub/home-assistant-addons/img_0.png']);

    // await browser.close()
})();

