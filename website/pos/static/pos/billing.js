Vue.component('suggestionrow', {

    props: [
        'rowData',
    ],

    delimiters: ['<%', '%>'],

    template: `<li class="suggestion" @click="suggestionselect"><% rowData.name %></li>`,

    methods: {
        suggestionselect: function() {
            this.rowData['qty'] = 1;
            vm.addProduct(this.rowData);
        }
    },

});



Vue.component('productrow', {

    props: [
        'rowData',
    ],

    delimiters: ['<%', '%>'],

    template: `
        <tr>
            <td class="product-id"><div><% rowData.id %></div></td>
            <td class="product-name"><div><% rowData.name %></div></td>
            <td class="product-mrp"><div><% rowData.mrp %></div></td>
            <td class="product-price"><div><% rowData.price %></div></td>
            <td class="product-qty"><a @click="qtydown" class="minus">-</a><div><% rowData.qty %></div><a @click="qtyup" class="plus">+</a></td>
            <td class="product-amt"><div><% rowData.qty * rowData.price %></div></td>
            <td class="product-delete"><div><button @click="remove">x</button></div></td>
        </tr>
    `,

    methods: {

        qtydown: function() {
            if (this.rowData.qty == 1) return
            this.rowData.qty--;
            vm.total -= this.rowData.price;
        },

        qtyup: function() {
            this.rowData.qty++;
            vm.total += this.rowData.price;
        },

        remove: function() {
            vm.total = vm.total - (this.rowData.price * this.rowData.qty);
            this.rowData.qty = 1;
            vm.products.splice(vm.products.indexOf(this.rowData), 1);

        },

    },

});






var vm = new Vue({

    el: '#app',

    delimiters: ['<%', '%>'],

    data: {

        query: '',

        contact: null,
        total: 0,
        paid: 0,

        products: [],
        suggestions: [],

    },

    computed: {

        balance: function() {
            return this.paid - this.total;
        }

    },

    methods: {

        closesuggestions: function() {
            this.suggestions = [];
        },

        // send request to backend asynchronously if query text has 4 or more chars
        searchQuery() {
            if (this.query.length < 4) {
                this.suggestions = [];
                return;
            }

            // URL to be replaced (Currently a sample json data file)
            url = "query/stockproducts?q=" + this.query;
            fetch(url)
                .then(response => {
                    if (!response.ok) throw 'Error';
                    return response.json();
                })
                .then(data => {
                    console.log(data);
                    this.suggestions = [];
                    for (i = 0; i < data.result.length; i++) this.suggestions.push(data.result[i]);
                })
                .catch(error => {
                    console.log('error: ', error);
                })
        },


        // FORMAT -- addProduct({ id: 007, name: 'James Bond', mrp: 100, price: 75, qty: 1 }) 
        addProduct: function(newProduct) {
            if (newProduct.qty == 0) return
            for (var i = 0; i < this.products.length; i++) {
                if (this.products[i].id == newProduct.id) {
                    newProduct.qty = this.products[i].qty + 1;
                    this.total += newProduct.price;
                    this.products.splice(i, 1);
                    this.products.unshift(newProduct);
                    return
                }
            }
            this.products.unshift(newProduct)
            this.total = this.total + (newProduct.price * newProduct.qty)
        },

        // to be completed as per backend requirement.
        // submit the form after the below actions.
        completeBill: function() {
            let billForm = new FormData();
            billForm.append('contact', this.contact);
            billForm.append('amount', this.total);
            billForm.append('isPaid', true);
            billForm.append('items', products);
        }

    },

});