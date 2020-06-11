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

        products: [
            { id: 1, name: 'Paracetamol', distributor: 'Inglecorp', stock: 123, visible: true },
            { id: 2, name: 'Dolo', distributor: 'Megham labs', stock: 234, visible: true },
        ],

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