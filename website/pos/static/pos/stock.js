Vue.component('suggestionrow', {

    props: [
        'rowData',
    ],

    delimiters: ['<%', '%>'],

    template: `<li class="suggestion" @click="suggestionselect"><% rowData.name %></li>`,

    methods: {
        suggestionselect: function() {
            vm.newproductsuggestions = []
            this.rowData['qty'] = 1;
            vm.selectedsuggestion = this.rowData;
            vm.newproductquery = '';
        }
    },

});



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
        distributors: [],

        newproductquery: '',
        newproductsuggestions: [],

        selectedsuggestion: null,
        selectedquantity: 0,
        selecteddistributor: 0,
        selectedcost: 0.0,
        selectedprice: 0.0,

    },

    methods: {

        closesuggestions: function() {
            this.newproductsuggestions = [];
        },

        queryproduct: function() {
            if (this.newproductquery.length < 4) {
                this.newproductsuggestions = [];
                return;
            }

            url = 'query/newproducts?q=' + this.newproductquery;
            fetch(url)
                .then(response => {
                    if (!response.ok) throw 'Error';
                    return response.json();
                })
                .then(data => {
                    console.log(data)
                    this.newproductsuggestions = [];
                    for (i = 0; i < data.result.length; i++) this.newproductsuggestions.push(data.result[i]);
                })
                .catch(error => {
                    console.log('error: ', error);
                })
        },

        addstock: function() {
            console.log('checkpoint 1');
            //if (this.selectedsuggestion == null || this.selectedquantity <= 0 || this.selecteddistibutor <= 0 || this.selectedcost <= 0 || this.selectedprice <= 0) return;
            console.log('checkpoint 2');
            var stockform = {};
            stockform['productid'] = this.selectedsuggestion['id'];
            stockform['distributorid'] = this.selecteddistributor;
            stockform['stock'] = this.selectedquantity;
            stockform['cost'] = this.selectedcost;
            stockform['price'] = this.selectedprice;
            console.log(stockform);

            fetch('addstock', {
                'method': 'POST',
                'body': JSON.stringify(stockform),
            })
            .then(response => {
                if(!response.ok) throw 'error';
                return response.json();
            })
            .then(data => {
                console.log(data['process']);
                if(data['process'] == 'Failure') {
                    alert('Failed to add to stock');
                } else {
                    alert(data['process']);
                    var flag = 0;
                    for(i = 0; i < this.products.length; i++) {
                        if(this.products[i].id == this.selectedsuggestion['id']) {
                            this.products[i].stock = this.products[i].stock + Number(this.selectedquantity);
                            flag = 1;
                        }
                    }
                    if(flag == 0) {
                        location.reload();
                    }

                    this.selectedsuggestion = null;
                    this.selectedquantity = 0;
                    this.selecteddistributor = 0;
                    this.selectedcost = 0.0;
                    this.selectedprice = 0.0;
                }
            })
        }

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