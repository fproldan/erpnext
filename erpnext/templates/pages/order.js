// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ready(function(){
	var loyalty_points_input = document.getElementById("loyalty-point-to-redeem");
	var loyalty_points_status = document.getElementById("loyalty-points-status");
	if (loyalty_points_input) {
		loyalty_points_input.onblur = apply_loyalty_points;
	}

	function apply_loyalty_points() {
		var loyalty_points = parseInt(loyalty_points_input.value);
		if (loyalty_points) {
			frappe.call({
				method: "erpnext.accounts.doctype.loyalty_program.loyalty_program.get_redeemption_factor",
				args: {
					"customer": doc_info.customer
				},
				callback: function(r) {
					if (r) {
						var message = ""
						let loyalty_amount = flt(r.message*loyalty_points);
						if (doc_info.grand_total && doc_info.grand_total < loyalty_amount) {
							let redeemable_amount = parseInt(doc_info.grand_total/r.message);
							message = "You can only redeem max " + redeemable_amount + " points in this order.";
							frappe.msgprint(__(message));
						} else {
							message = loyalty_points + " Loyalty Points of amount "+ loyalty_amount + " is applied."
							frappe.msgprint(__(message));
							var remaining_amount = flt(doc_info.grand_total) - flt(loyalty_amount);
							var payment_button = document.getElementById("pay-for-order");
							payment_button.innerHTML = __("Pay Remaining");
							payment_button.href = "/api/method/erpnext.accounts.doctype.payment_request.payment_request.make_payment_request?dn="+doc_info.doctype_name+"&dt="+doc_info.doctype+"&loyalty_points="+loyalty_points+"&submit_doc=1&order_type=Shopping Cart";
						}
						loyalty_points_status.innerHTML = message;
					}
				}
			});
		}
	}
})


frappe.ready(function() {
    var $form = $("form[id='frmFileUp']");

    $form.on("change", "[type='file']", function(e) {
      var $input = $(this);
      var input = $input.get(0);
      
      if(input.files.length) {

        input.filedata = {"files_data" : []};

        window.file_reading = true;

        $.each(input.files, function(key, value) {
          setupReader(value, input);
        });

        window.file_reading = false;
      }

      if (e.target.files.length) {
        $(this).next('.custom-file-label').html(e.target.files[0].name);
      }
    });

    $("#btn_upload").click(function(e) {
      var filedata = $('#select_files').prop('filedata');
      console.log(filedata)
      if (!filedata) {
      	frappe.msgprint("Seleccione un archivo");
      	e.preventDefault();
      } else {
      	frappe.call({
	        method: "erpnext.templates.pages.order.attach_file_to_po",
	        args: {"files": JSON.stringify(filedata), "docname": "{{ docname }}"},
	        freeze: true,
	        freeze_message: __("Adjuntando archivo..."),
	        callback: function(r){
	          if(!r.exc) {
	            frappe.msgprint("Archivo adjuntado");
	          } else {
	            frappe.msgprint("Archivo no adjuntado. <br /> " + r.exc);
	          }
	        }
	      });
      }
    });
  });

  function setupReader(file, input) {
      var name = file.name;
      var reader = new FileReader();  
      reader.onload = function(e) {
      input.filedata.files_data.push({
        "__file_attachment": 1,
        "filename": file.name,
        "dataurl": reader.result
      })
    }
    reader.readAsDataURL(file);
  }