
const app = {
    users: {
        admin: {
            username: 'admin',
            password: 'admin123',
            role: 'admin',
            total_purchases: 0,
            membership: null
        }
    },
    currentUser: null,
    cart: [],
    products: [
        {id: 1, name: 'Mixer', price: 450000, status: 'Available', category: 'Kitchen appliances'},
        {id: 2, name: 'Oven', price: 2500000, status: 'Available', category: 'Kitchen appliances'},
        {id: 3, name: 'Blender', price: 350000, status: 'Available', category: 'Kitchen appliances'},
        {id: 4, name: 'Microwave', price: 800000, status: 'Available', category: 'Kitchen appliances'},
        {id: 5, name: 'Refrigerator', price: 3500000, status: 'Available', category: 'Kitchen appliances'},
        {id: 6, name: 'Vacuum Cleaner', price: 1200000, status: 'Available', category: 'Cleaning devices'},
        {id: 7, name: 'Robot Vacuum', price: 2800000, status: 'Available', category: 'Cleaning devices'},
        {id: 8, name: 'Air Conditioner', price: 4500000, status: 'Available', category: 'Heating and cooling devices'},
        {id: 9, name: 'Heater', price: 650000, status: 'Available', category: 'Heating and cooling devices'},
        {id: 10, name: 'Fan', price: 280000, status: 'Available', category: 'Heating and cooling devices'},
        {id: 11, name: 'Hair Dryer', price: 180000, status: 'Available', category: 'Personal care devices'},
        {id: 12, name: 'Electric Shaver', price: 320000, status: 'Available', category: 'Personal care devices'},
        {id: 13, name: 'Smart Speaker', price: 550000, status: 'Available', category: 'Smart home devices'},
        {id: 14, name: 'Smart Doorbell', price: 780000, status: 'Available', category: 'Smart home devices'},
        {id: 15, name: 'Smart Thermostat', price: 920000, status: 'Available', category: 'Smart home devices'}
    ],
    DELIVERY_FEE: 50000
};


function scrollToOptions() {
    document.getElementById('optionsSection').scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
    });
}

function formatPrice(price) {
    return `${price.toLocaleString()} UZS`;
}

function print(text, className = '') {
    const terminal = document.getElementById('terminal');
    const output = document.createElement('div');
    output.className = `output ${className}`;
    output.textContent = text;
    terminal.appendChild(output);
    terminal.scrollTop = terminal.scrollHeight;
}

function clearTerminal() {
    const terminal = document.getElementById('terminal');
    terminal.innerHTML = '';
}

const ZIP_FILE = 'document.zip'

const FLOWCHART_PDF = 'flow-chart.pdf';


const PY_FILES = ['index.py', 'auth.py', 'cart.py', 'database.py', 'membership.py'];

function downloadFlowchartFile() {
    const a = document.createElement('a');
    a.href = encodeURI(FLOWCHART_PDF);
    a.download = FLOWCHART_PDF;
    document.body.appendChild(a);
    a.click();
    a.remove();
}
function downloadZipFile() {
    const a = document.createElement('a');
    a.href = encodeURI(ZIP_FILE);
    a.download = ZIP_FILE;
    document.body.appendChild(a);
    a.click();
    a.remove();
}

function downloadAllPythonFiles() {
    PY_FILES.forEach((filename, i) => {

        setTimeout(() => {
            const a = document.createElement('a');
            a.href = encodeURI(filename);
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
        }, i * 150);
    });
}



function startTerminal() {
    const container = document.getElementById('terminalContainer');
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth' });
    
    clearTerminal();
    
    setTimeout(() => {
        print('='.repeat(70));
        print('WELCOME TO TECH HOUSE - Home Appliance Store');
        print('='.repeat(70));
        print('');
        setTimeout(() => showAuthMenu(), 500);
    }, 500);
}

function showAuthMenu() {
    print('='.repeat(70));
    print('TECH HOUSE');
    print('='.repeat(70));
    print('');
    print('1. Login');
    print('2. Register');
    print('3. Continue as guest');
    print('0. Exit');
    print('');
    promptInput('Select: ', handleAuthChoice);
}

function handleAuthChoice(choice) {
    if (choice === '1') {
        promptLogin();
    } else if (choice === '2') {
        promptRegister();
    } else if (choice === '3') {
        showMainMenu();
    } else if (choice === '0') {
        print('');
        print('='.repeat(70));
        print('THANK YOU FOR VISITING TECH HOUSE!');
        print('='.repeat(70));
        print('');
        print('Refresh the page to start again', 'info');
    } else {
        print('Invalid choice', 'error');
        print('');
        showAuthMenu();
    }
}

function promptLogin() {
    print('='.repeat(70));
    print('LOGIN');
    print('='.repeat(70));
    print('');
    promptInput('Username: ', (username) => {
        promptInput('Password: ', (password) => {
            if (app.users[username] && app.users[username].password === password) {
                app.currentUser = app.users[username];
                print('');
                print('Login successful!', 'success');
                print('');
                setTimeout(() => showMainMenu(), 1000);
            } else {
                print('');
                print('Invalid username or password', 'error');
                print('');
                setTimeout(() => showAuthMenu(), 1500);
            }
        });
    });
}

function promptRegister() {
    print('='.repeat(70));
    print('REGISTER');
    print('='.repeat(70));
    print('');
    promptInput('Username: ', (username) => {
        if (app.users[username]) {
            print('');
            print('Username already exists', 'error');
            print('');
            setTimeout(() => showAuthMenu(), 1500);
        } else {
            promptInput('Password: ', (password) => {
                app.users[username] = {
                    username: username,
                    password: password,
                    role: 'customer',
                    membership: null,
                    total_purchases: 0
                };
                print('');
                print('Registration successful!', 'success');
                print('');
                setTimeout(() => showAuthMenu(), 1500);
            });
        }
    });
}

function showMainMenu() {
    print('');
    print('='.repeat(70));
    print('MAIN MENU');
    print('='.repeat(70));
    print('');
    
    if (app.currentUser) {
        print(`Logged in: ${app.currentUser.username}`);
        if (app.currentUser.membership) {
            print(`Membership: ${app.currentUser.membership}`);
        }
    } else {
        print('Guest Mode');
    }
    
    print(`Cart: ${app.cart.length} items`);
    print('');
    print('1. View all products');
    print('2. Search products');
    print('3. View cart');
    print('4. Add to cart');
    if (app.currentUser) {
        print('5. Set membership');
        print('6. Checkout');
        print('99. Logout');
    }
    print('0. Exit');
    print('');
    
    promptInput('Select: ', handleMainMenuChoice);
}

function handleMainMenuChoice(choice) {
    if (choice === '1') {
        showProducts();
    } else if (choice === '2') {
        searchProducts();
    } else if (choice === '3') {
        viewCart();
    } else if (choice === '4') {
        addToCart();
    } else if (choice === '5' && app.currentUser) {
        setMembership();
    } else if (choice === '6' && app.currentUser) {
        checkout();
    } else if (choice === '99' && app.currentUser) {
        app.currentUser = null;
        print('');
        print('Logged out successfully', 'success');
        print('');
        setTimeout(() => showAuthMenu(), 1000);
    } else if (choice === '0') {
        print('');
        print('='.repeat(70));
        print('THANK YOU FOR VISITING TECH HOUSE!');
        print('='.repeat(70));
        print('');
        print('Refresh the page to start again', 'info');
    } else {
        print('');
        print('Invalid choice or feature not available', 'error');
        print('');
        setTimeout(() => showMainMenu(), 1000);
    }
}

function showProducts() {
    print('');
    print('='.repeat(70));
    print('AVAILABLE PRODUCTS');
    print('='.repeat(70));
    print('');
    
    const categories = {};
    app.products.filter(p => p.status === 'Available').forEach(product => {
        if (!categories[product.category]) {
            categories[product.category] = [];
        }
        categories[product.category].push(product);
    });
    
    Object.keys(categories).forEach(category => {
        print(`\n${category}:`, 'info');
        categories[category].forEach(product => {
            print(`  ID: ${product.id} | ${product.name} | ${formatPrice(product.price)}`);
        });
    });
    
    print('');
    setTimeout(() => showMainMenu(), 100);
}

function searchProducts() {
    print('');
    promptInput('Enter search term: ', (keyword) => {
        print('');
        print('Search Results:', 'info');
        print('-'.repeat(70));
        
        const results = app.products.filter(p => 
            p.name.toLowerCase().includes(keyword.toLowerCase()) ||
            p.category.toLowerCase().includes(keyword.toLowerCase())
        );
        
        if (results.length > 0) {
            results.forEach(product => {
                print(`ID: ${product.id} | ${product.name} | ${formatPrice(product.price)}`);
            });
        } else {
            print('No products found', 'error');
        }
        
        print('');
        setTimeout(() => showMainMenu(), 100);
    });
}

function addToCart() {
    print('');
    print('Available products:');
    app.products.filter(p => p.status === 'Available').forEach(product => {
        print(`ID: ${product.id} | ${product.name} | ${formatPrice(product.price)}`);
    });
    print('');
    
    promptInput('Enter product ID (0 to cancel): ', (id) => {
        const product = app.products.find(p => p.id === parseInt(id) && p.status === 'Available');
        if (product) {
            app.cart.push(product);
            updateCartBadge();
            print('');
            print(`${product.name} added to cart!`, 'success');
            print('');
        } else if (id !== '0') {
            print('');
            print('Invalid product ID', 'error');
            print('');
        }
        setTimeout(() => showMainMenu(), 1000);
    });
}

function viewCart() {
    print('');
    print('='.repeat(70));
    print('SHOPPING CART');
    print('='.repeat(70));
    print('');
    
    if (app.cart.length === 0) {
        print('Your cart is empty');
    } else {
        let total = 0;
        app.cart.forEach((item, index) => {
            let price = item.price;
            if (app.currentUser && app.currentUser.membership) {
                const discounts = {Bronze: 5, Silver: 10, Gold: 15};
                const discount = discounts[app.currentUser.membership] || 0;
                price = price * (1 - discount / 100);
            }
            total += price;
            print(`${index + 1}. ${item.name} - ${formatPrice(price)}`);
        });
        
        if (app.currentUser && app.currentUser.membership === 'Gold') {
            print('');
            print('Delivery: FREE (Gold Membership)');
        } else {
            print('');
            print(`Delivery: ${formatPrice(app.DELIVERY_FEE)}`);
            total += app.DELIVERY_FEE;
        }
        
        print('-'.repeat(70));
        print(`TOTAL: ${formatPrice(total)}`);
    }
    
    print('');
    setTimeout(() => showMainMenu(), 100);
}

function setMembership() {
    print('');
    print('='.repeat(70));
    print('SELECT MEMBERSHIP');
    print('='.repeat(70));
    print('');
    print('1. Bronze (5% discount)');
    print('2. Silver (10% discount)');
    print('3. Gold (15% discount + Free delivery)');
    print('0. Cancel');
    print('');
    
    promptInput('Select: ', (choice) => {
        const packages = {1: 'Bronze', 2: 'Silver', 3: 'Gold'};
        if (packages[choice]) {
            app.currentUser.membership = packages[choice];
            print('');
            print(`Membership set to ${packages[choice]}!`, 'success');
            print('');
        }
        setTimeout(() => showMainMenu(), 1000);
    });
}

function checkout() {
    if (app.cart.length === 0) {
        print('');
        print('Your cart is empty', 'error');
        print('');
        setTimeout(() => showMainMenu(), 1000);
        return;
    }
    
    print('');
    print('='.repeat(70));
    print('CHECKOUT');
    print('='.repeat(70));
    print('');
    
    let total = 0;
    app.cart.forEach(item => {
        let price = item.price;
        if (app.currentUser.membership) {
            const discounts = {Bronze: 5, Silver: 10, Gold: 15};
            const discount = discounts[app.currentUser.membership] || 0;
            price = price * (1 - discount / 100);
        }
        total += price;
    });
    
    if (app.currentUser.membership !== 'Gold') {
        total += app.DELIVERY_FEE;
    }
    
    print(`Total Amount: ${formatPrice(total)}`);
    print('');
    
    promptInput('Confirm checkout? (yes/no): ', (confirm) => {
        if (confirm.toLowerCase() === 'yes') {
            app.currentUser.total_purchases += app.cart.length;
            app.cart.forEach(item => {
                const product = app.products.find(p => p.id === item.id);
                if (product) product.status = 'Sold';
            });
            app.cart = [];
            updateCartBadge();
            
            print('');
            print('ORDER COMPLETED SUCCESSFULLY!', 'success');
            print(`Total purchases: ${app.currentUser.total_purchases}`, 'info');
            print('');
        } else {
            print('');
            print('Order cancelled', 'info');
            print('');
        }
        setTimeout(() => showMainMenu(), 2000);
    });
}

function promptInput(promptText, callback) {
    const terminal = document.getElementById('terminal');
    const inputLine = document.createElement('div');
    inputLine.className = 'input-line';
    inputLine.innerHTML = `<span class="prompt">${promptText}</span><input type="text" id="terminalInput" autocomplete="off"><span class="cursor"></span>`;
    terminal.appendChild(inputLine);
    
    const input = inputLine.querySelector('input');
    input.focus();
    terminal.scrollTop = terminal.scrollHeight;
    
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const value = input.value;
            inputLine.innerHTML = `<span class="prompt">${promptText}</span>${value}`;
            callback(value);
        }
    });
}

function updateCartBadge() {
    const badge = document.getElementById('cartCount');
    if (badge) {
        badge.textContent = app.cart.length;
    }
}


document.addEventListener('DOMContentLoaded', () => {
    console.log('Tech House Application Loaded');
    updateCartBadge();
});