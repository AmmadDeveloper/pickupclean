function remove(id){
    if (+id > -1) { // only splice array when item is found
      cart.splice(+id, 1); // 2nd parameter means remove one item only
    }
    updateRows()
}
function addtocart(id){
    var item=cart[id]
    if(!item.total>0){
        alert("Please enter correct details")
    }else{
        var token=localStorage.getItem('token')
        $.ajax({
            url: '/api/cart',
            type: 'post',
            headers:{'Authorization': `Bearer ${token}`},
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                cart[id].qty=data.cartitem.qty;
                cart[id].name=data.cartitem.name;
                cart[id].id=data.cartitem.id;
                cart[id].catid=data.cartitem.catid;
                cart[id].cartid=data.cartitem.cartid;
                cart[id].total=data.cartitem.total;
                cart[id].price=data.cartitem.price;
                cart[id].catname=data.cartitem.catname;
                UserCart=[...UserCart,data.cartitem]
                updateCart()
                updateRows()
            },
            data: JSON.stringify(item)
        });
    }
}
var cart=[
    {
        "cartid":0,
        "catid":"",
        "catname":"",
        "name":"",
        "id":"",
        "price":"0",
        "qty":0,
        "total":0
    }
]
var obj={
    "cartid":0,
    "catid":"",
    "catname":"",
    "name":"",
    "id":"",
    "price":"0",
    "qty":0,
    "total":0
}
function checkout(){
    var data=JSON.stringify(cart)
    $.post("/api/cart",data,function (res){
       console.log(res);
    });
}
function updateRows(){
    let rows=""
    if(cart.length>0) {
        $.each(cart, (key, value) => {
            rows += `<div style="display: inline-block" class="form-group">
                  <select onchange="getService('service${key}',this,${key})" name="category${key}" id="category${key}" style=" display: inline-block;height: 43px">
                      ${genCat(value.catid)}
                  </select>
                  <select  id="service${key}" name="service${key}" onchange="getPrice('service${key}','price${key}','qty${key}','${key}')" style="display: inline-block;height: 43px">${genService(value.id, value.catid)}</select>
                    <input onchange="getPrice('service${key}','price${key}','qty${key}','${key}')" style="display: inline-block;width: 100px;" type="number" name="qty${key}" required="" id="qty${key}" min="1" value="${value.qty !== 0 ? value.qty : 1}"/>
                    <input style="display: inline-block;width: 100px;" type="text" readonly name="price${key}" required="" id="price${key}" value="${value.total !== 0 ? "£"+value.total.toString() : "£0"}"/>`
            if (value.cartid === 0) {
                rows += `<span>
                        <button type="button" onclick="addtocart(${key})" style="background-color: orange;display: inline-block; color: white" class="btn"><i class="fa fa-check"></i></button>
                        <button type="button" onclick="remove(${key})" style="background-color: orange;display: inline-block; color: white" class="btn"><i class="fa fa-times"></i></button>
                    </span>`
            } else {
                rows += `<span>
                        <button type="button" onclick="editcart(${key},${value.cartid})" style="background-color: orange;display: inline-block; color: white" class="btn"><i class="fa fa-edit"></i></button>
                        <button type="button" onclick="removecart(${value.cartid})" style="background-color: orange;display: inline-block; color: white" class="btn"><i class="fa fa-times"></i></button>
                    </span>`
            }
            rows += `</div>`
        });
        $("#detail-rows")[0].innerHTML = rows;
    }
}


function editcart(id,cartid){
    var item=cart[id]
    if(!item.total>0){
        alert("Please enter correct details")
    }else{
        var token=localStorage.getItem('token')
        $.ajax({
            url: '/api/cart',
            type: 'patch',
            headers:{'Authorization': `Bearer ${token}`},
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                cart[id].qty=data.cartitem.qty;
                cart[id].name=data.cartitem.name;
                cart[id].id=data.cartitem.id;
                cart[id].catid=data.cartitem.catid;
                cart[id].cartid=data.cartitem.cartid;
                cart[id].total=data.cartitem.total;
                cart[id].price=data.cartitem.price;
                cart[id].catname=data.cartitem.catname;
                UserCart=UserCart.filter(x=>x.cartid!==data.cartitem.cartid)
                UserCart=[...UserCart,data.cartitem]
                updateCart()
            },
            data: JSON.stringify(item)
        });
    }
}


function removecart(cartid){
    var token=localStorage.getItem('token')
    $.ajax({
        url: `/api/cart?cartid=${cartid}`,
        type: 'delete',
        headers:{'Authorization': `Bearer ${token}`},
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            UserCart=UserCart.filter((x)=>x.cartid!==cartid);
            cart=cart.filter((x)=>x.cartid!==cartid);
            updateCart()
            updateRows()
        }
    });

}
function genService(id,catid){
    let serv='<option value="">Select a Service </option>'
    if(catid!==''){
         $.ajaxSetup({async: false});
         $.get('/api/services/?id='+catid,function(res){

            $.each(res,function (key,val){
               if (val.id!==+id) {
                   serv += `<option value="${val.price}-${val.id}">${val.name}</option>`
               }else {
                   serv += `<option value="${val.price}-${val.id}" selected>${val.name}</option>`
               }
           });

        });

    }
    return serv
}
function genCat(id){
    var res='<option value="">Select a Category </option>'
    $.each(cats,function (key,val){
        if (val.id===+id){
            res+=`<option value="${val.id}" selected>${val.name}</option>`
        }
        else{
            res+=`<option value="${val.id}">${val.name}</option>`
        }
       });
    if(id!==''){
        $(`#${id}`).change();
    }
    return res;
}
function getPrice(sid,priceid,qtyid,index){
    var price=+($(`#${sid}`)[0].value.split('-')[0])
    var qty=+$(`#${qtyid}`)[0].value
    $(`#${priceid}`)[0].value="£"+(price*qty).toString()
    cart[index].price=price;
    cart[index].qty=qty;
    cart[index].total=price*qty;
    cart[index].id=$(`#${sid}`)[0].value.split('-')[1]
    cart[index].name=$(`#${sid}`)[0].options[$(`#${sid}`)[0].selectedIndex].text;
}
function addRow(){
    cart=[...cart,{...obj}]
    updateRows()
}



$.get('/api/categories/',function(res){
    cats=res;
    updateRows();
});
$(document).ready(function(){

    var token=localStorage.getItem('token')
    $.ajax({
        url: '/api/cart',
        type: 'get',
        headers:{'Authorization': `Bearer ${token}`},
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            if(data.length!==0){
                cart=data;
                UserCart=data;
                updateRows()
                updateCart()
            }

        }
    });

});
var UserCart=[]
function updateCart(){
    let rows=""
    $.each(UserCart,(key,value)=>{
        rows+=`<div class="row">
                  <div class="col-sm-7">${value.qty} X ${value.name} - ${value.catname}</div>
                  <div style="text-align: right" class="col-sm-5">
                      £${value.total}
                  </div>
              </div>`
    });
    $("#total-amount")[0].innerHTML=UserCart.reduce((x,y)=>x+y.total,0);
    $("#ord-info__content")[0].innerHTML=rows;

}
function getService(service,cat,index){
    cart[index].catid=cat.value;
    var si=cat.selectedIndex;
    cart[index].catname=cat.options[si].text;
    var selection=cat.value;
    if(selection!==''){
        $.get('/api/services/?id='+selection,function(res){
        var serv='<option value="">Select a Service </option>'
       $.each(res,function (key,val){
           serv+=`<option value="${val.price}-${val.id}">${val.name}</option>`
       });
        $(`#${service}`)[0].innerHTML=serv;
    });
    }
}
function addItem(){
    var cat=$("#category")[0].value;
    var catname=$("#category")[0].options[$('#category')[0].selectedIndex].innerText
    var serv=$("#service")[0].value.split('-');
    var serid=+serv[1];
    var sername=$("#service")[0].options[$('#service')[0].selectedIndex].innerText;
    var price=+serv[0];
    var qty=+$('#qty')[0].value;
    var obj={
        "catid":cat,
        "catname":catname,
        "name":sername,
        "id":serid,
        "price":price,
        "qty":qty,
        "total":price*qty
    }
    cart.push(obj);

    var items="";
    $.each(cart,function (key,val){
       items+=`${val.qty} X ${val.name}-${val.catname}    €${val.total}`
    });

}