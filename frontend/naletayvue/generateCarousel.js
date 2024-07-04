import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Получение текущей директории
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Указание правильного пути к папке с каруселями
const carouselDir = path.join(__dirname, 'src/assets/carousels');
const publicCarouselDir = path.join(__dirname, 'public/carousels');

function generateCarouselData() {
    // Получение всех категорий каруселей
    const categories = fs.readdirSync(carouselDir).filter(folder => {
        const folderPath = path.join(carouselDir, folder);
        return fs.lstatSync(folderPath).isDirectory();
    });

    categories.forEach(carouselCategory => {
        const categoryDir = path.join(carouselDir, carouselCategory);
        const categoryPublicDir = path.join(publicCarouselDir, carouselCategory);

        // Проверка существования директории
        if (!fs.existsSync(categoryDir)) {
            console.error(`Directory not found: ${categoryDir}`);
            return;
        }

        if (!fs.existsSync(categoryPublicDir)) {
            fs.mkdirSync(categoryPublicDir, { recursive: true });
        }

        const carouselFolders = fs.readdirSync(categoryDir).filter(folder => {
            const folderPath = path.join(categoryDir, folder);
            return fs.lstatSync(folderPath).isDirectory();
        });

        const carouselData = [];

        carouselFolders.forEach(folder => {
            const folderPath = path.join(categoryDir, folder);
            const mobileImage = path.join(folderPath, 'mobile.png');
            const tabletImage = path.join(folderPath, 'tablet.png');
            const desktopImage = path.join(folderPath, 'desktop.png');
            const textFile = path.join(folderPath, 'data.json');

            if (fs.existsSync(desktopImage) && fs.existsSync(textFile)) {
                try {
                    const fileContent = fs.readFileSync(textFile, 'utf8');
                    const textData = JSON.parse(fileContent);

                    const copyImage = (src, dest) => {
                        if (fs.existsSync(src)) {
                            fs.copyFileSync(src, dest);
                        }
                    };

                    const publicFolder = path.join(categoryPublicDir, folder);
                    if (!fs.existsSync(publicFolder)) {
                        fs.mkdirSync(publicFolder, { recursive: true });
                    }

                    copyImage(mobileImage, path.join(publicFolder, 'mobile.png'));
                    copyImage(tabletImage, path.join(publicFolder, 'tablet.png'));
                    copyImage(desktopImage, path.join(publicFolder, 'desktop.png'));

                    carouselData.push({
                        mobileImage: fs.existsSync(mobileImage) ? `carousels/${carouselCategory}/${folder}/mobile.png` : `carousels/${carouselCategory}/${folder}/desktop.png`,
                        tabletImage: fs.existsSync(tabletImage) ? `carousels/${carouselCategory}/${folder}/tablet.png` : `carousels/${carouselCategory}/${folder}/desktop.png`,
                        desktopImage: `carousels/${carouselCategory}/${folder}/desktop.png`,
                        title: textData.title,
                        text: textData.text,
                        color: textData.color,
                        btn: textData.btn,
                        link: textData.link || '#'
                    });
                } catch (error) {
                    console.error(`Error parsing JSON in folder ${folderPath}:`, error.message);
                }
            }
        });

        fs.writeFileSync(path.join(categoryDir, 'carouselData.json'), JSON.stringify(carouselData, null, 2));
        console.log(`Carousel data for ${carouselCategory} generated successfully!`);
    });
}

// Запуск генерации данных для всех категорий каруселей
generateCarouselData();
