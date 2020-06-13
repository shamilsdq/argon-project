Vue.component('product-row', {

    props: [
        'product',
    ],

    delimiters: ['<%', '%>'],

    template: `
        <tr>
                <td class="cell-id"><% product.id %></td>
                <td><% product.name %></td>
                <td><% product.distributor %></td>
                <td class="cell-stock"><% product.stock %></td>
        </tr>
    `,

});




var vm = new Vue({

    el: '#app',

    delimiters: ['<%', '%>'],

    data: {

        searchtext: '',
        products: [],

        newproductquery: '',
        newproductsuggestions: [],
        selectedsuggestion: null

    },

    methods: {
        queryproduct: function() {
            if (this.newproductquery.length < 4) {
                this.newproductsuggestions = [];
                return;
            }

            url = '#';
            fetch(url)
                .then(response => {
                    if (!response.ok) throw 'Error';
                    return response.json();
                })
                .then(data => {
                    this.newproductsuggestions = [];
                    for (i = 0; i < data.products.length; i++) this.newproductsuggestions.push(data.products[i]);
                })
                .catch(error => {
                    console.log('error: ', error);
                })
        },
    },

    watch: {
        searchtext: function() {
            for (i = 0; i < this.products.length; i++) {
                if (this.products[i].name.toLowerCase().search(this.searchtext.toLowerCase()) == -1 && this.products[i].distributor.toLowerCase().search(this.searchtext.toLowerCase())) {
                    this.products[i].visible = false
                } else {
                    this.products[i].visible = true
                }
            }
        }
    },

})