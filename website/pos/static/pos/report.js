Vue.component('billrow', {

    props: [
        'billdata',
    ],

    delimiters: ['<%', '%>'],

    template: `
        <tr @click="selectbill()">
                <td class="cell-id"><% billdata.id %></td>
                <td class="cell-contact"><% billdata.contact %></td>
                <td class="cell-amount"><% billdata.amount %></td>
        </tr>
    `,

    methods: {
        selectbill: function() {
            vm.getitems(this.billdata)
        },
    }

});



var vm = new Vue({

    el: '#app',
    delimiters: ['<%', '%>'],

    data: {
        searchtext: '',
        bills: [],
        billdetails: null,
    },

    methods: {
        getitems: function(billdata) {
            if(this.billdetails != null) {
                if(this.billdetails.id == billdata.id) return;
            }
            url = 'query/billdetails?q=' + billdata.id
            fetch(url)
                .then(response => {
                    if (!response.ok) throw 'Error';
                    return response.json();
                })
                .then(data => {
                    this.billdetails = {'id': billdata.id, 'contact': billdata.contact, 'amount': billdata.amount, 'items': []}
                    for(i = 0; i < data.result.length; i++) {
                        this.billdetails.items.push({'name': data.result[i].product, 'quantity': data.result[i].quantity});
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        },
    },

    watch: {
        searchtext: function() {
            for(i = 0; i < this.bills.length; i++) {
                if(this.bills[i].id.toString().search(this.searchtext) == -1 && this.bills[i].contact.toString().search(this.searchtext) == -1) {
                    this.bills[i].visible = false;
                } else {
                    this.bills[i].visible = true;
                }
            }
        }
    },

});