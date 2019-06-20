function get_or_create(rec, bins, value)
  if aerospike:exists(rec) then
    return false
  else
    rec["owner"] = bins["owner"]
    status = aerospike:create(rec)
    return true
  end
end